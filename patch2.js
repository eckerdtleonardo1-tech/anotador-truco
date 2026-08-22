const fs = require('fs');

let content = fs.readFileSync('index.html', 'utf-8');

// 1. Add Chart.js to HEAD
if (!content.includes('chart.js')) {
    content = content.replace('</head>', '  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>');
}

// 2. Add Buttons to Bottom Actions
const new_buttons = `
    <button onclick="openDeck()" class="flex items-center gap-1 text-zinc-600 hover:text-zinc-300 transition-colors py-2 px-3 rounded-full hover:bg-zinc-800/40 text-xs font-semibold">
      🃏 Mazo
    </button>
    <div class="w-px h-4 bg-zinc-800"></div>
    <button onclick="showGraph()" class="flex items-center gap-1 text-zinc-600 hover:text-zinc-300 transition-colors py-2 px-3 rounded-full hover:bg-zinc-800/40 text-xs font-semibold">
      📈 Gráfico
    </button>
    <div class="w-px h-4 bg-zinc-800"></div>
`;
// find the Stats button and append next to it
content = content.replace('Stats\n    </button>\n    <div class="w-px h-4 bg-zinc-800"></div>', 'Stats\n    </button>\n    <div class="w-px h-4 bg-zinc-800"></div>' + new_buttons);

// 3. Modals HTML
const modals_html = `
  <!-- Gráfico Modal -->
  <div id="graph-modal" class="hidden-el fixed inset-0 bg-black/85 backdrop-blur-md flex items-center justify-center z-[60] p-4">
    <div class="modal-enter bg-zinc-900 border border-zinc-800/70 rounded-3xl p-5 w-full max-w-2xl shadow-2xl relative">
      <button onclick="document.getElementById('graph-modal').classList.add('hidden-el')" class="absolute top-4 right-4 text-zinc-400 hover:text-white text-xl font-bold">×</button>
      <h3 class="text-center font-bold text-lg mb-4 text-zinc-200 uppercase tracking-widest">Evolución de la Partida</h3>
      <div class="w-full bg-zinc-800/50 rounded-xl p-2 h-64 sm:h-80">
        <canvas id="scoreChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Mazo Modal -->
  <div id="deck-modal" class="hidden-el fixed inset-0 bg-black/85 backdrop-blur-md flex flex-col items-center justify-center z-[60] p-4">
    <button onclick="document.getElementById('deck-modal').classList.add('hidden-el')" class="absolute top-4 right-4 text-zinc-400 hover:text-white text-3xl font-bold">×</button>
    
    <div class="bg-zinc-900 border border-zinc-800/70 rounded-3xl p-6 w-full max-w-md shadow-2xl flex flex-col items-center">
      <h3 class="font-bold text-xl mb-6 text-zinc-200">Mazo de Truco</h3>
      
      <div id="cards-container" class="flex gap-3 mb-8 justify-center min-h-[160px]">
        <!-- Cards go here -->
      </div>
      
      <button onclick="dealCards()" class="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 rounded-2xl text-white font-bold text-sm shadow-lg transition-all active:scale-95 flex items-center justify-center gap-2">
        Repartir 3 cartas
      </button>
      <p class="text-xs text-zinc-500 mt-4 text-center">Toca las cartas para voltearlas. Ideal si te quedaste sin mazo físico.</p>
    </div>
  </div>
`;
content = content.replace('<!-- Winner Modal -->', modals_html + '\n  <!-- Winner Modal -->');

// 4. JS Logic for Deck and Graph
const js_logic = `
  // --- GRÁFICO ---
  let chartInstance = null;
  function showGraph() {
    document.getElementById('graph-modal').classList.remove('hidden-el');
    const ctx = document.getElementById('scoreChart').getContext('2d');
    
    if (chartInstance) chartInstance.destroy();
    
    let labels = state.scoreHistory.map((_, i) => 'Acción ' + i);
    let datasets = [];
    const colors = ['#3b82f6', '#f59e0b', '#10b981']; // blue, amber, emerald
    
    for (let i = 0; i < state.mode; i++) {
        datasets.push({
            label: state.teams[i],
            data: state.scoreHistory.map(h => h[i]),
            borderColor: colors[i],
            backgroundColor: colors[i] + '40',
            tension: 0.3,
            fill: true,
            borderWidth: 3,
            pointRadius: 2
        });
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: state.limit, ticks: { color: '#a1a1aa' }, grid: { color: '#27272a' } },
                x: { ticks: { display: false }, grid: { display: false } }
            },
            plugins: {
                legend: { labels: { color: '#e4e4e7', font: { family: 'Inter', weight: 'bold' } } }
            }
        }
    });
  }

  // --- MAZO VIRTUAL ---
  const suits = [
      { name: 'Espada', emoji: '⚔️', color: 'text-blue-600' },
      { name: 'Basto', emoji: '🪵', color: 'text-green-700' },
      { name: 'Oro', emoji: '🪙', color: 'text-yellow-600' },
      { name: 'Copa', emoji: '🍷', color: 'text-red-600' }
  ];
  const values = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12];
  let deck = [];
  
  function initDeck() {
      deck = [];
      for (let s of suits) {
          for (let v of values) {
              deck.push({ v: v, s: s });
          }
      }
      // Shuffle
      deck.sort(() => Math.random() - 0.5);
      deck.sort(() => Math.random() - 0.5);
  }

  function dealCards() {
      if (deck.length < 3) initDeck();
      let hand = [deck.pop(), deck.pop(), deck.pop()];
      
      const container = document.getElementById('cards-container');
      container.innerHTML = hand.map((c, i) => \`
          <div class="relative w-20 sm:w-24 h-32 sm:h-36 cursor-pointer transform transition-transform hover:scale-105 active:scale-95" onclick="this.querySelector('.card-front').classList.toggle('hidden'); this.querySelector('.card-back').classList.toggle('hidden'); haptic(10);">
             <!-- Reverso (Oculta) -->
             <div class="card-back absolute inset-0 bg-blue-900 rounded-xl shadow-lg border-2 border-white/20 flex flex-col items-center justify-center p-1 bg-[radial-gradient(circle,_transparent_20%,_#1e3a8a_20%,_#1e3a8a_80%,_transparent_80%,_transparent),radial-gradient(circle,_transparent_20%,_#1e3a8a_20%,_#1e3a8a_80%,_transparent_80%,_transparent)_25px_25px] bg-[length:50px_50px]">
                <div class="w-full h-full border border-blue-400/30 rounded-lg"></div>
             </div>
             <!-- Frente (Visible) -->
             <div class="card-front hidden absolute inset-0 bg-white rounded-xl shadow-xl flex flex-col items-center justify-center border-2 border-zinc-200">
                <span class="text-2xl sm:text-3xl font-black \${c.s.color}">\${c.v}</span>
                <span class="text-3xl sm:text-4xl mt-2 drop-shadow-md">\${c.s.emoji}</span>
             </div>
          </div>
      \`).join('');
      
      playTick(400, 0.1);
      haptic(20);
  }

  function openDeck() {
      document.getElementById('deck-modal').classList.remove('hidden-el');
      document.getElementById('cards-container').innerHTML = ''; // Limpiar mesa
      initDeck();
  }
`;
content = content.replace('// Nuevas Funciones', js_logic + '\n  // Nuevas Funciones');

// 5. Update History Tracker
// Find load() to init scoreHistory
const load_inject = `
      if(!state.scoreHistory) state.scoreHistory = [[...state.scores]];
`;
content = content.replace("if(state.theme === undefined) state.theme = 'dark';", "if(state.theme === undefined) state.theme = 'dark';" + load_inject);

// Add to resetGame()
content = content.replace('state.scores=[0,0,0];', 'state.scores=[0,0,0]; state.scoreHistory=[[0,0,0]];');

// Add to changeScore()
content = content.replace('state.scores[idx]=Math.max(0,state.scores[idx]+amount);', 'state.scores[idx]=Math.max(0,state.scores[idx]+amount);\n    state.scoreHistory.push([...state.scores]);');

// Add to undoLast()
content = content.replace('state.scores=prev.scores;', 'state.scores=prev.scores; if(state.scoreHistory && state.scoreHistory.length > 1) state.scoreHistory.pop();');


fs.writeFileSync('index.html', content, 'utf-8');
console.log('Parche aplicado.');
