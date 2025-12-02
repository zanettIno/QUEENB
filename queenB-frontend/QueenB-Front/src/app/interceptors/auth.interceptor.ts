// src/app/interceptors/auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const token = authService.getToken();

  // Clone a requisição e adiciona o token JWT no header
  let authReq = req;
  if (token) {
    authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  // Processa a requisição e trata erros
  return next(authReq).pipe(
    catchError((error) => {
      // Se receber 401 (Unauthorized), faz logout
      if (error.status === 401) {
        console.error('Token inválido ou expirado. Realizando logout...');
        authService.logoutLocal();
        router.navigate(['/login']);
      }

      // Se receber 403 (Forbidden)
      if (error.status === 403) {
        console.error('Acesso negado');
      }

      // Retorna o erro para ser tratado pelo componente
      return throwError(() => error);
    })
  );
};