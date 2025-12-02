// src/app/pages/login/login.component.ts
import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, Router, ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  username = '';
  password = '';
  passwordVisible: boolean = false;
  loading = false;
  errorMessage = '';
  returnUrl = '';

  ngOnInit(): void {
    // Se já estiver autenticado, redireciona
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/home']);
    }

    // Pega URL de retorno
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home';
  }

  onSubmit() {
    if (!this.username || !this.password) {
      this.errorMessage = 'Por favor, preencha todos os campos';
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    // Chama o backend
    this.authService.login({
      email: this.username,
      senha: this.password
    }).subscribe({
      next: (response) => {
        console.log('Login realizado com sucesso:', response);
        this.router.navigate([this.returnUrl]);
      },
      error: (error) => {
        console.error('Erro no login:', error);
        this.loading = false;

        if (error.status === 401) {
          this.errorMessage = 'Email ou senha incorretos';
        } else if (error.status === 0) {
          this.errorMessage = 'Erro de conexão com o servidor';
        } else {
          this.errorMessage = 'Erro ao realizar login. Tente novamente.';
        }
      }
    });
  }

  togglePasswordVisibility(): void {
    this.passwordVisible = !this.passwordVisible;
  }
}