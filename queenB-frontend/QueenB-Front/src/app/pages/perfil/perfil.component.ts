// src/app/pages/perfil/perfil.component.ts
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { UsuarioEdicao } from '../../interfaces/backend.models';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './perfil.component.html',
  styleUrl: './perfil.component.css'
})
export class PerfilComponent implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);

  // Variáveis para o formulário
  perfil = {
    usuario: '',
    email: '',
    senha: '',
    confirmarSenha: ''
  };

  loading = false;
  successMessage = '';
  errorMessage = '';

  ngOnInit(): void {
    // Carrega dados do usuário atual
    const user = this.authService.getCurrentUser();
    if (user) {
      this.perfil.usuario = user.nome;
      this.perfil.email = user.email;
    } else {
      // Se não tem usuário, busca do backend
      this.authService.getMe().subscribe({
        next: (user) => {
          this.perfil.usuario = user.nome;
          this.perfil.email = user.email;
        },
        error: (error) => {
          console.error('Erro ao carregar perfil:', error);
        }
      });
    }
  }

  salvarPerfil() {
    this.errorMessage = '';
    this.successMessage = '';

    // Validações
    if (this.perfil.senha && this.perfil.senha !== this.perfil.confirmarSenha) {
      this.errorMessage = 'As senhas não coincidem';
      return;
    }

    if (this.perfil.senha && this.perfil.senha.length < 6) {
      this.errorMessage = 'A senha deve ter no mínimo 6 caracteres';
      return;
    }

    this.loading = true;

    // Prepara dados para atualização
    const dadosAtualizacao: UsuarioEdicao = {
      nome: this.perfil.usuario,
      email: this.perfil.email
    };

    // Adiciona senha apenas se foi preenchida
    if (this.perfil.senha) {
      dadosAtualizacao.senha = this.perfil.senha;
    }

    // Chama o backend
    this.authService.editar(dadosAtualizacao).subscribe({
      next: (response) => {
        console.log('Perfil atualizado:', response);
        this.loading = false;
        this.successMessage = 'Perfil atualizado com sucesso!';
        
        // Limpa campos de senha
        this.perfil.senha = '';
        this.perfil.confirmarSenha = '';

        // Remove mensagem de sucesso após 3 segundos
        setTimeout(() => {
          this.successMessage = '';
        }, 3000);
      },
      error: (error) => {
        console.error('Erro ao atualizar perfil:', error);
        this.loading = false;

        if (error.status === 400) {
          this.errorMessage = error.error?.detail || 'Email já cadastrado por outro usuário';
        } else {
          this.errorMessage = 'Erro ao atualizar perfil. Tente novamente.';
        }
      }
    });
  }

  fechar() {
    this.router.navigate(['/home']);
  }
}