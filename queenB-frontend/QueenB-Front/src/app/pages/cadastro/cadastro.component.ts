// src/app/pages/cadastro/cadastro.component.ts
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-cadastro',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './cadastro.component.html',
  styleUrl: './cadastro.component.css'
})
export class CadastroComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  username = '';
  email = '';
  password = '';
  confirmPassword = '';

  passwordVisible: boolean = false;
  confirmPasswordVisible: boolean = false;
  loading = false;
  errorMessage = '';

  onSubmit() {
    // Validações
    if (!this.username || !this.email || !this.password || !this.confirmPassword) {
      this.errorMessage = 'Por favor, preencha todos os campos';
      return;
    }

    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'As senhas não coincidem';
      return;
    }

    if (this.password.length < 6) {
      this.errorMessage = 'A senha deve ter no mínimo 6 caracteres';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    // Chama o backend
    this.authService.cadastrar({
      nome: this.username,
      email: this.email,
      senha: this.password
    }).subscribe({
      next: (response) => {
        console.log('Cadastro realizado com sucesso:', response);
        // Redireciona para home (usuário já está logado após cadastro)
        this.router.navigate(['/home']);
      },
      error: (error) => {
        console.error('Erro no cadastro:', error);
        this.loading = false;

        if (error.status === 400) {
          this.errorMessage = error.error.detail || 'Email já cadastrado';
        } else if (error.status === 0) {
          this.errorMessage = 'Erro de conexão com o servidor';
        } else {
          this.errorMessage = 'Erro ao realizar cadastro. Tente novamente.';
        }
      }
    });
  }

  togglePasswordVisibility(): void {
    this.passwordVisible = !this.passwordVisible;
  }

  toggleConfirmPasswordVisibility(): void {
    this.confirmPasswordVisible = !this.confirmPasswordVisible;
  }
}