import sys
content = open('index.html', 'r', encoding='utf-8').read()

# 1. Add CSS animations and themes
css_additions = '''
    /* Nuevos Temas y Animaciones */
    @keyframes drawMatch { from { max-height: 0; opacity: 0; } to { max-height: 18px; opacity: 1; } }
    .match-stick, .match-diagonal { animation: drawMatch 0.2s ease-out forwards; }
    
    body.theme-pano { background: #1a472a; color: #f4f4f5; }
    body.theme-pano .bg-zinc-900\\/60 { background: #0f331c; border-color: #276b3f; }
    body.theme-pano .main-btn { background: #133f23; border-color: #276b3f; }
    
    body.theme-boca { background: #001a4d; color: #ffcc00; }
    body.theme-boca .bg-zinc-900\\/60 { background: #000d26; border-color: #ffcc00; }
    body.theme-boca .main-btn { background: #001a4d; border-color: #ffcc00; color: #ffcc00; }
    
    body.theme-river { background: #ffffff; color: #ff0000; }
    body.theme-river .bg-zinc-900\\/60 { background: #f0f0f0; border-color: #ff0000; }
    body.theme-river .main-btn { background: #ffffff; border-color: #ff0000; color: #18181b; }
    
    .locked-ui { pointer-events: none; filter: blur(2px) grayscale(50%); opacity: 0.6; transition: all 0.3s; }
'''
content = content.replace('</style>', css_additions + '\n  </style>')

# 2. Add 40 limit button
limit_btns = '''<button id="btn-limit-30" class="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all bg-blue-600 text-white" onclick="setLimit(30)">30</button>
        <button id="btn-limit-40" class="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all text-zinc-500" onclick="setLimit(40)">40</button>'''
content = content.replace('<button id="btn-limit-30" class="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all bg-blue-600 text-white" onclick="setLimit(30)">30</button>', limit_btns)

# 3. Add Lock and Fullscreen to header buttons
header_buttons = '''<!-- Fullscreen -->
      <button onclick="toggleFullScreen()" class="flex items-center justify-center p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50 transition-colors" title="Pantalla Completa">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>
      </button>
      <!-- Lock -->
      <button onclick="toggleLock()" id="btn-lock" class="flex items-center justify-center p-1.5 rounded-lg text-zinc-500 hover:text-zinc-300 hover:bg-zinc-800/50 transition-colors" title="Bloquear Mesa">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
      </button>'''
content = content.replace('<!-- Sound Toggle -->', header_buttons + '\n      <!-- Sound Toggle -->')

# 4. Give IDs to Falta Envido buttons and add dice to inputs
for i in range(1, 4):
    content = content.replace(f'onclick="faltaEnvido({i})" class="quick-btn', f'id="btn-falta-envido-{i}" onclick="faltaEnvido({i})" class="quick-btn')
    input_str = f'onkeydown="if(event.key===\'Enter\') saveTeam({i})">'
    dice_btn = f'<button onclick="randomName({i})" class="ml-1 text-sm bg-zinc-800 hover:bg-zinc-700 px-1.5 rounded" title="Nombre aleatorio">🎲</button>'
    content = content.replace(input_str, input_str + dice_btn)

# 5. Add Stats and Random Mano to Bottom actions
bottom_actions = '''<button onclick="showStats()" class="flex items-center gap-1 text-zinc-600 hover:text-zinc-300 transition-colors py-2 px-3 rounded-full hover:bg-zinc-800/40 text-xs font-semibold">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
      Stats
    </button>
    <div class="w-px h-4 bg-zinc-800"></div>
    <button onclick="randomMano()" class="flex items-center gap-1 text-zinc-600 hover:text-zinc-300 transition-colors py-2 px-3 rounded-full hover:bg-zinc-800/40 text-xs font-semibold">
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><circle cx="15.5" cy="15.5" r="1.5"></circle></svg>
      Mano
    </button>
    <div class="w-px h-4 bg-zinc-800"></div>'''
content = content.replace('<button onclick="toggleHistory()"', bottom_actions + '\n    <button onclick="toggleHistory()"')

# 6. Add JS logic
js_additions = '''
  // Nuevas Funciones
  let isLocked = false;
  function toggleLock() {
    isLocked = !isLocked;
    document.getElementById('main-board').classList.toggle('locked-ui', isLocked);
    document.getElementById('btn-lock').innerHTML = isLocked 
        ? '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
        : '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 9.9-1"></path></svg>';
    if(isLocked) showToast('Mesa bloqueada');
    else showToast('Mesa desbloqueada');
  }

  function toggleFullScreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => {});
    } else {
        if (document.exitFullscreen) document.exitFullscreen();
    }
  }

  const randomNames = ['Los Auténticos', 'Falta Envido', 'Tirame las Cartas', 'El Rey', 'Mentiras', 'Los de Afuera', 'Sin Señas', 'Canto Flor', 'Pica Pica'];
  function randomName(t) {
    const inp = document.getElementById(`team${t}-input`);
    inp.value = randomNames[Math.floor(Math.random() * randomNames.length)];
    saveTeam(t);
  }

  function randomMano() {
    state.manoIdx = Math.floor(Math.random() * state.mode);
    haptic(20);
    showToast(`Mano sorteada: ${state.teams[state.manoIdx]}`);
    updateWithTransition();
  }
  
  function showStats() {
    let totalPartidas = wins.reduce((a,b)=>a+b, 0);
    let t = `🏆 ESTADÍSTICAS GLOBALES\\n\\n`;
    t += `Partidas Jugadas: ${totalPartidas}\\n`;
    for(let i=0; i<state.mode; i++) {
        t += `Victorias ${state.teams[i]}: ${wins[i]}\\n`;
    }
    alert(t);
  }

  // Voces
  function speakAction(label) {
     if(!soundEnabled || !label) return;
     try {
       let u = new SpeechSynthesisUtterance(label);
       u.lang = 'es-AR';
       u.rate = 1.2;
       speechSynthesis.speak(u);
     } catch(e){}
  }
'''
content = content.replace('function haptic(ms) {', js_additions + '\n  function haptic(ms) {')

# Voice call inside changeScore
content = content.replace("addLog(idx,amount,label||'');", "addLog(idx,amount,label||''); if(label) speakAction(label);")

# Dynamic Falta Envido logic in updateUI
dynamic_falta = '''
    const half = state.limit === 15 ? 0 : state.limit / 2;
    let maxScore = Math.max(...state.scores.slice(0, state.mode));
    let pointsToAdd = (maxScore < half) ? state.limit : (state.limit - maxScore);
    for(let i=1; i<=3; i++) {
        const fBtn = document.getElementById(`btn-falta-envido-${i}`);
        if(fBtn) fBtn.innerHTML = `Falta E.<br><span class="q-sub text-[11px] sm:text-xs opacity-60">+${pointsToAdd}</span>`;
    }
'''
content = content.replace('for(let i=1; i<=3; i++) {', dynamic_falta + '\n    for(let i=1; i<=3; i++) {')

# Theme cycle logic
cycle_logic = '''
  const themes = ['dark', 'light', 'pano', 'boca', 'river'];
  function toggleTheme() {
    let currentIdx = themes.indexOf(state.theme);
    state.theme = themes[(currentIdx + 1) % themes.length];
    applyTheme();
    save();
  }
  function applyTheme() {
    document.body.className = 'antialiased select-none';
    if(state.theme === 'light') document.body.classList.add('light-mode');
    else if(state.theme === 'pano') document.body.classList.add('theme-pano');
    else if(state.theme === 'boca') document.body.classList.add('theme-boca');
    else if(state.theme === 'river') document.body.classList.add('theme-river');
    
    const icon = document.getElementById('theme-icon-dark');
    if(icon) {
        if(state.theme === 'dark') icon.innerHTML = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>';
        else if(state.theme === 'light') icon.innerHTML = '<circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>';
        else icon.innerHTML = '<circle cx="12" cy="12" r="10"></circle><path d="M12 2v20"></path>'; // generic icon for custom themes
    }
    const metaTheme = document.querySelector('meta[name="theme-color"]');
    if(metaTheme) {
        if(state.theme === 'light') metaTheme.setAttribute('content', '#f4f4f5');
        else if(state.theme === 'pano') metaTheme.setAttribute('content', '#1a472a');
        else if(state.theme === 'boca') metaTheme.setAttribute('content', '#001a4d');
        else if(state.theme === 'river') metaTheme.setAttribute('content', '#ffffff');
        else metaTheme.setAttribute('content', '#0a0a0c');
    }
  }
'''
content = content.replace('function toggleTheme() {', 'function oldToggleTheme() {')
content = content.replace('function applyTheme() {', 'function oldApplyTheme() {')
content = content.replace('function oldToggleTheme() {', cycle_logic + '\n  function oldToggleTheme() {')


# 40 Limit Toggle in updateUI
limit_toggles = '''
    if(state.limit === 15) { setToggle('btn-limit-15', 'btn-limit-30'); document.getElementById('btn-limit-40').className="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all text-zinc-500"; }
    else if(state.limit === 30) { setToggle('btn-limit-30', 'btn-limit-15'); document.getElementById('btn-limit-40').className="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all text-zinc-500"; }
    else if(state.limit === 40) { setToggle('btn-limit-40', 'btn-limit-15'); document.getElementById('btn-limit-30').className="tog-btn px-2 sm:px-3 py-1 rounded-md text-[11px] sm:text-xs font-bold transition-all text-zinc-500"; }
'''
content = content.replace("if(state.limit===15) setToggle('btn-limit-15','btn-limit-30'); else setToggle('btn-limit-30','btn-limit-15');", limit_toggles)


open('index.html', 'w', encoding='utf-8').write(content)
print('Modificaciones aplicadas con éxito.')
