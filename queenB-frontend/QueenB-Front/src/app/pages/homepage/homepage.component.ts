// src/app/pages/homepage/homepage.component.ts
import { Component, AfterViewInit, inject, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import * as L from 'leaflet';
import { PathService } from '../../services/path.service';
import { AirportService } from '../../services/airport.service';
import { AeroportoResposta, RespostaCaminho } from '../../interfaces/backend.models';

@Component({
  selector: 'app-homepage',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './homepage.component.html',
  styleUrl: './homepage.component.css'
})
export class HomepageComponent implements AfterViewInit, OnInit, OnDestroy {
  private pathService = inject(PathService);
  private airportService = inject(AirportService);

  // Variáveis do Dropdown
  isDropdownOpen: boolean = false;
  filterOptions: string[] = ['Menor Distância (Dijkstra)', 'Menos Paradas (BFS)', 'Comparar Algoritmos'];
  selectedFilter: string = 'Menor Distância (Dijkstra)';

  // Variáveis de busca
  origem: string = '';
  destino: string = '';
  
  // Variável do Mapa
  private map: L.Map | null = null;
  private routeLayer: L.Polyline | null = null;
  private markers: L.Marker[] = [];

  // Lista de aeroportos para autocomplete (opcional)
  aeroportos: AeroportoResposta[] = [];

  // Resultado da busca
  resultadoCaminho: RespostaCaminho | null = null;
  errorMessage: string = '';
  loading: boolean = false;

  ngOnInit(): void {
    // Carrega lista de aeroportos
    this.airportService.listarAtivos().subscribe({
      next: (response) => {
        this.aeroportos = response.aeroportos;
        console.log('Aeroportos carregados:', this.aeroportos.length);
      },
      error: (error) => {
        console.error('Erro ao carregar aeroportos:', error);
      }
    });
  }

  ngAfterViewInit(): void {
    this.initMap();
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
    }
  }

  // Função que cria o mapa
  private initMap(): void {
    // Corrige o problema dos ícones do Leaflet
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    
    // Usa ícones padrão do CDN se não tiver local
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    });

    this.map = L.map('map', { 
      center: [-14.235, -51.9253], // Centro do Brasil
      zoom: 4 
    });

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 3,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
      
    // Correção do bug do mapa "quebrado"
    setTimeout(() => {
      this.map?.invalidateSize();
    }, 100);
  }

  // Funções do Dropdown
  toggleDropdown(): void {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  selectFilter(option: string): void {
    this.selectedFilter = option;
    this.isDropdownOpen = false; 
  }

  // Trocar origem e destino
  trocarOrigemDestino(): void {
    const temp = this.origem;
    this.origem = this.destino;
    this.destino = temp;
  }

  // Função principal de busca
  mostrarRota(): void {
    // Limpa mensagens anteriores
    this.errorMessage = '';
    this.resultadoCaminho = null;

    // Validações
    if (!this.origem.trim() || !this.destino.trim()) {
      this.errorMessage = 'Por favor, preencha origem e destino';
      return;
    }

    const origemUpper = this.origem.trim().toUpperCase();
    const destinoUpper = this.destino.trim().toUpperCase();

    if (origemUpper === destinoUpper) {
      this.errorMessage = 'Origem e destino devem ser diferentes';
      return;
    }

    // Valida formato IATA (3 letras)
    if (origemUpper.length !== 3 || destinoUpper.length !== 3) {
      this.errorMessage = 'Use códigos IATA válidos (3 letras). Ex: GRU, GIG, BSB';
      return;
    }

    this.loading = true;

    // Escolhe algoritmo baseado no filtro selecionado
    if (this.selectedFilter.includes('Dijkstra')) {
      this.calcularDijkstra(origemUpper, destinoUpper);
    } else if (this.selectedFilter.includes('BFS')) {
      this.calcularBFS(origemUpper, destinoUpper);
    } else {
      this.compararAlgoritmos(origemUpper, destinoUpper);
    }
  }

  private calcularDijkstra(origem: string, destino: string): void {
    this.pathService.calcularMenorCaminho(origem, destino).subscribe({
      next: (response) => {
        this.resultadoCaminho = response;
        this.desenharRotaNoMapa(response);
        this.loading = false;
      },
      error: (error) => {
        console.error('Erro ao calcular rota:', error);
        this.handleError(error);
        this.loading = false;
      }
    });
  }

  private calcularBFS(origem: string, destino: string): void {
    this.pathService.calcularCaminhoBFS(origem, destino).subscribe({
      next: (response) => {
        this.resultadoCaminho = response;
        this.desenharRotaNoMapa(response);
        this.loading = false;
      },
      error: (error) => {
        console.error('Erro ao calcular rota:', error);
        this.handleError(error);
        this.loading = false;
      }
    });
  }

  private compararAlgoritmos(origem: string, destino: string): void {
    this.pathService.compararAlgoritmos(origem, destino).subscribe({
      next: (response) => {
        console.log('Comparação:', response);
        // Mostra Dijkstra no mapa por padrão
        this.resultadoCaminho = response.dijkstra;
        this.desenharRotaNoMapa(response.dijkstra);
        this.loading = false;
        
        // Exibe comparação
        const metricas = this.pathService.compararMetricas(response.dijkstra, response.bfs);
        console.log('Métricas:', metricas);
        
        const mensagem = `Comparação de Algoritmos:\n\n` +
          `📍 Dijkstra (Menor Distância):\n` +
          `   • ${response.dijkstra.distancia_total_km} km\n` +
          `   • ${response.dijkstra.numero_paradas} parada(s)\n\n` +
          `📍 BFS (Menos Paradas):\n` +
          `   • ${response.bfs.distancia_total_km} km\n` +
          `   • ${response.bfs.numero_paradas} parada(s)\n\n` +
          `✅ Recomendação: ${metricas.recomendacao}`;
        
        alert(mensagem);
      },
      error: (error) => {
        console.error('Erro ao comparar algoritmos:', error);
        this.handleError(error);
        this.loading = false;
      }
    });
  }

  private handleError(error: any): void {
    if (error.status === 0) {
      this.errorMessage = 'Erro de conexão com o servidor. Verifique se o backend está rodando.';
    } else if (error.status === 404) {
      this.errorMessage = error.error?.mensagem || 'Rota não encontrada entre os aeroportos informados.';
    } else if (error.error?.mensagem) {
      this.errorMessage = error.error.mensagem;
    } else {
      this.errorMessage = 'Não foi possível calcular o caminho. Verifique os códigos IATA.';
    }
  }

  private desenharRotaNoMapa(resposta: RespostaCaminho): void {
    if (!this.map) return;

    // Remove rota e marcadores anteriores
    this.limparMapa();

    // Busca coordenadas dos aeroportos no caminho
    const promises = resposta.caminho.map(aeroporto => {
      return this.airportService.buscarPorCodigo(aeroporto.codigo_iata).toPromise();
    });

    Promise.all(promises).then(results => {
      const coords: L.LatLngTuple[] = [];
      
      results.forEach((result, index) => {
        if (result && result.aeroportos.length > 0) {
          const aero = result.aeroportos[0];
          if (aero.latitude && aero.longitude) {
            coords.push([aero.latitude, aero.longitude]);
            
            // Cria ícone customizado para origem/destino
            const isFirst = index === 0;
            const isLast = index === results.length - 1;
            
            // Adiciona marcador
            const marker = L.marker([aero.latitude, aero.longitude])
              .addTo(this.map!)
              .bindPopup(`
                <strong>${aero.codigo_iata}</strong><br>
                ${aero.nome}<br>
                <small>${aero.cidade || ''} ${aero.pais ? '- ' + aero.pais : ''}</small>
                ${isFirst ? '<br><span style="color: green">📍 Origem</span>' : ''}
                ${isLast ? '<br><span style="color: red">🏁 Destino</span>' : ''}
              `);
            
            this.markers.push(marker);
            
            // Abre popup no primeiro e último
            if (isFirst || isLast) {
              marker.openPopup();
            }
          }
        }
      });

      // Desenha a linha da rota
      if (coords.length > 1) {
        this.routeLayer = L.polyline(coords, {
          color: '#E47E02',
          weight: 4,
          opacity: 0.8,
          dashArray: '10, 10'
        }).addTo(this.map!);

        // Ajusta zoom para mostrar toda a rota
        this.map!.fitBounds(this.routeLayer.getBounds(), { padding: [50, 50] });
      }
    }).catch(error => {
      console.error('Erro ao buscar coordenadas:', error);
      this.errorMessage = 'Erro ao desenhar rota no mapa.';
    });
  }

  private limparMapa(): void {
    // Remove polyline anterior
    if (this.routeLayer && this.map) {
      this.map.removeLayer(this.routeLayer);
      this.routeLayer = null;
    }

    // Remove marcadores anteriores
    this.markers.forEach(marker => {
      if (this.map) {
        this.map.removeLayer(marker);
      }
    });
    this.markers = [];
  }

  // Métodos de formatação para o template
  formatarCaminhoExibicao(): string {
    if (!this.resultadoCaminho) return '';
    return this.resultadoCaminho.caminho
      .map(a => a.codigo_iata)
      .join(' → ');
  }

  formatarTempoExibicao(): string {
    if (!this.resultadoCaminho) return '';
    const minutos = this.resultadoCaminho.tempo_estimado_min;
    const horas = Math.floor(minutos / 60);
    const mins = minutos % 60;
    
    if (horas === 0) return `${mins}min`;
    if (mins === 0) return `${horas}h`;
    return `${horas}h ${mins}min`;
  }
}