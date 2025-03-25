import os
import argparse
from pathlib import Path
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TransferSpeedColumn
)
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

load_dotenv()
console = Console()

class GofileUploader:
    def __init__(self):
        self.api_key = os.getenv('GOFILE_API_KEY')
        self.base_url = "https://api.gofile.io"
        self.server = None
        self.results = []
        self.progress = None

    def get_server(self):
        """Fetch optimal server for uploads"""
        try:
            response = requests.get(f"{self.base_url}/servers", timeout=10)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 'ok' and data['data']['servers']:
                self.server = data['data']['servers'][0]['name']
            else:
                raise Exception("No available servers")
        except Exception as e:
            console.print(f"[red]Server Error: {str(e)}[/]")
            raise

    def create_progress(self):
        """Configure progress display with all components"""
        return Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=40, style="blue", complete_style="bright_green"),
            TaskProgressColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console,
            transient=True
        )

    def upload_file(self, file_path):
        """Upload file with real progress tracking"""
        try:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            task_id = self.progress.add_task(
                "upload",
                filename=file_name,
                start=False,
                total=file_size
            )
            
            with open(file_path, "rb") as f:
                fields = [('file', (file_name, f))]
                if self.api_key: fields.append(('token', self.api_key))
                
                encoder = MultipartEncoder(fields=fields)
                monitor = MultipartEncoderMonitor(
                    encoder,
                    lambda m: self.progress.update(
                        task_id,
                        advance=m.bytes_read - self.progress.tasks[task_id].completed
                    )
                )
                
                self.progress.start_task(task_id)
                response = requests.post(
                    f"https://{self.server}.gofile.io/uploadFile",
                    data=monitor,
                    headers={'Content-Type': monitor.content_type},
                    timeout=30
                )

            if response.json()['status'] == 'ok':
                result = response.json()['data']
                self.results.append(result)
                return True
            return False
            
        except Exception as e:
            self.progress.stop_task(task_id)
            console.print(f"[red]Error uploading {file_name}: {str(e)}[/]")
            return False

    def process_path(self, path):
        """Handle files and directories recursively"""
        path = Path(path)
        if path.is_file():
            self.upload_file(path)
        elif path.is_dir():
            for item in path.iterdir():
                self.process_path(item)

    def upload(self, paths):
        """Main upload control flow"""
        try:
            with self.create_progress() as progress:
                self.progress = progress
                self.get_server()
                for path in paths:
                    self.process_path(path)
        finally:
            # Show final results
            for result in self.results:
                console.print(Panel(
                    f"File: [bold]{result['name']}[/]\n"
                    f"Download: [link={result['downloadPage']}]{result['downloadPage']}[/]",
                    title="[green]✓ Upload Complete[/]",
                    border_style="dim"
                ))

def main():
    parser = argparse.ArgumentParser(description='Gofile Uploader with Rich Progress')
    parser.add_argument('paths', nargs='+', help='Files/directories to upload')
    args = parser.parse_args()

    uploader = GofileUploader()
    try:
        uploader.upload(args.paths)
    except KeyboardInterrupt:
        console.print("\n[red]Upload cancelled by user![/]")
    except Exception as e:
        console.print(f"[red]Fatal Error: {str(e)}[/]")

if __name__ == "__main__":
    main()
