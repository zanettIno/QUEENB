// src/app/services/auth.service.ts
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  UsuarioCadastro,
  UsuarioLogin,
  UsuarioEdicao,
  UsuarioResposta,
  TokenResposta,
  MensagemResposta
} from '../interfaces/backend.models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;
  
  // Observable para status de autenticação
  private currentUserSubject = new BehaviorSubject<UsuarioResposta | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();
  
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();

  constructor() {
    // Verifica se existe token no localStorage ao inicializar
    this.checkAuthentication();
  }

  // ========================
  // AUTHENTICATION METHODS
  // ========================

  /**
   * Cadastra novo usuário
   */
  cadastrar(dados: UsuarioCadastro): Observable<TokenResposta> {
    return this.http
      .post<TokenResposta>(`${this.apiUrl}/usuarios/cadastro`, dados)
      .pipe(
        tap(response => {
          this.setSession(response);
        })
      );
  }

  /**
   * Realiza login
   */
  login(dados: UsuarioLogin): Observable<TokenResposta> {
    return this.http
      .post<TokenResposta>(`${this.apiUrl}/usuarios/login`, dados)
      .pipe(
        tap(response => {
          this.setSession(response);
        })
      );
  }

  /**
   * Obtém dados do usuário autenticado
   */
  getMe(): Observable<UsuarioResposta> {
    return this.http
      .get<UsuarioResposta>(`${this.apiUrl}/usuarios/me`)
      .pipe(
        tap(user => {
          this.currentUserSubject.next(user);
        })
      );
  }

  /**
   * Edita dados do usuário autenticado
   */
  editar(dados: UsuarioEdicao): Observable<UsuarioResposta> {
    return this.http
      .put<UsuarioResposta>(`${this.apiUrl}/usuarios/editar`, dados)
      .pipe(
        tap(user => {
          this.currentUserSubject.next(user);
          // Atualiza localStorage
          localStorage.setItem('user', JSON.stringify(user));
        })
      );
  }

  /**
   * Realiza logout
   */
  logout(): Observable<MensagemResposta> {
    return this.http
      .post<MensagemResposta>(`${this.apiUrl}/usuarios/logout`, {})
      .pipe(
        tap(() => {
          this.clearSession();
        })
      );
  }

  /**
   * Logout local (sem chamar API)
   */
  logoutLocal(): void {
    this.clearSession();
  }

  // ========================
  // SESSION MANAGEMENT
  // ========================

  private setSession(authResult: TokenResposta): void {
    localStorage.setItem('access_token', authResult.access_token);
    localStorage.setItem('user', JSON.stringify(authResult.usuario));
    
    this.currentUserSubject.next(authResult.usuario);
    this.isAuthenticatedSubject.next(true);
  }

  private clearSession(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    
    this.currentUserSubject.next(null);
    this.isAuthenticatedSubject.next(false);
  }

  private checkAuthentication(): void {
    const token = this.getToken();
    const userStr = localStorage.getItem('user');
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        this.currentUserSubject.next(user);
        this.isAuthenticatedSubject.next(true);
      } catch (e) {
        this.clearSession();
      }
    }
  }

  // ========================
  // UTILITY METHODS
  // ========================

  /**
   * Retorna o token JWT
   */
  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Verifica se usuário está autenticado
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  /**
   * Retorna dados do usuário atual
   */
  getCurrentUser(): UsuarioResposta | null {
    return this.currentUserSubject.value;
  }

  /**
   * Retorna ID do usuário atual
   */
  getCurrentUserId(): number | null {
    const user = this.getCurrentUser();
    return user ? user.id_usuario : null;
  }

  /**
   * Retorna email do usuário atual
   */
  getCurrentUserEmail(): string | null {
    const user = this.getCurrentUser();
    return user ? user.email : null;
  }

  /**
   * Retorna nome do usuário atual
   */
  getCurrentUserName(): string | null {
    const user = this.getCurrentUser();
    return user ? user.nome : null;
  }
}