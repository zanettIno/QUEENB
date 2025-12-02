import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
// 1. TEM QUE TER ISSO
import { RouterLink, RouterLinkActive } from '@angular/router'; 

@Component({
  selector: 'app-sidebar',
  standalone: true,
  // 2. TEM QUE TER ISSO NOS IMPORTS
  imports: [CommonModule, RouterLink, RouterLinkActive], 
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {

}