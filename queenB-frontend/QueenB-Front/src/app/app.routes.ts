// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

// Páginas principais
import { LoginComponent } from './pages/login/login.component';
import { CadastroComponent } from './pages/cadastro/cadastro.component';

// A "Moldura" (Pai)
import { HomeComponent } from './pages/home/home.component'; 

// As "Telas" (Filhos)
import { HomepageComponent } from './pages/homepage/homepage.component';
import { GerRotasComponent } from './pages/ger-rotas/ger-rotas.component';
import { AeroportosComponent } from './pages/aeroportos/aeroportos.component';
import { PerfilComponent } from './pages/perfil/perfil.component';

export const routes: Routes = [
    { path: 'login', component: LoginComponent },
    { path: 'cadastro', component: CadastroComponent },
    
    // ROTA "PAI" (A MOLDURA) - PROTEGIDA
    { 
      path: 'home', 
      component: HomeComponent,
      canActivate: [authGuard], // 🔒 PROTEGIDO
      children: [
        { path: '', component: HomepageComponent }, 
        { path: 'rotas', component: GerRotasComponent },
        { path: 'aeroportos', component: AeroportosComponent },
        { path: 'perfil', component: PerfilComponent }
      ]
    },
    
    // Redirecionamento padrão
    { path: '', redirectTo: 'login', pathMatch: 'full' }
];