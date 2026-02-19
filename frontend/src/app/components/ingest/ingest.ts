import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-ingest',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ingest.html',
  styleUrls: ['./ingest.scss'],
})
export class Ingest {
  selectedFile: File | null = null;
  isUploading = false;
  message: string | null = null;
  error: string | null = null;

  constructor(private api: ApiService) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.message = null;
      this.error = null;
    }
  }

  uploadFile() {
    if (!this.selectedFile) return;

    this.isUploading = true;
    this.message = null;
    this.error = null;

    this.api.ingest(this.selectedFile).subscribe({
      next: (res) => {
        this.message = `Fichier "${this.selectedFile?.name}" ajouté avec succès au RAG.`;
        this.selectedFile = null;
        this.isUploading = false;

        // Reset file input
        const fileInput = document.getElementById('fileUpload') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      },
      error: (err) => {
        console.error(err);
        this.error = "Erreur lors de l'envoi du fichier.";
        this.isUploading = false;
      },
    });
  }
}
