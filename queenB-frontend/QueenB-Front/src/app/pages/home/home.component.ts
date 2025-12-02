import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router'; // 1. TEM QUE TER ISSO
import { SidebarComponent } from '../../components/sidebar/sidebar.component';

@Component({
  selector: 'app-home',
  standalone: true,
  // 2. TEM QUE TER ISSO NOS IMPORTS
  imports: [CommonModule, RouterOutlet, SidebarComponent], 
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  // Vazio! A lógica do mapa foi movida para o 'homepage.component'
}