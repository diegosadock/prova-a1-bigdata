from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'src/base.html'
s=p.read_text(encoding='utf-8')

def replace_once(old,new):
 global s
 n=s.count(old)
 assert n==1,(old[:90],n)
 s=s.replace(old,new,1)

replace_once('<option value="game">Show do Milhão</option>', '<option value="practice">Treinar / Simulados</option><option value="cases">Missões práticas</option><option value="game">Show do Milhão</option>')
replace_once('<button class="navbtn" data-nav="game"><span class="ico">♛</span>Show do Milhão</button>', '<button class="navbtn" data-nav="practice"><span class="ico">▣</span>Treino e simulados</button><button class="navbtn" data-nav="cases"><span class="ico">⚡</span>Missões práticas</button><button class="navbtn" data-nav="game"><span class="ico">♛</span>Show do Milhão</button>')
replace_once('flashRevealed:false,lessonHelp:', 'flashRevealed:false,training:null,practiceTopic:"Todos",practiceDifficulty:"0",practiceSize:"15",casesIndex:0,casesSelected:null,caseRight:saved.caseRight||{},caseWrong:saved.caseWrong||{},lessonHelp:')
replace_once('games:state.games}))','games:state.games,caseRight:state.caseRight,caseWrong:state.caseWrong}))')
replace_once("lab:'Laboratório',game:'Show do Milhão'", "lab:'Laboratório',practice:'Treino e simulados',cases:'Missões práticas',game:'Show do Milhão'")
replace_once("lab:renderLab,game:renderGame", "lab:renderLab,practice:renderPractice,cases:renderCases,game:renderGame")
replace_once('${DATA.lessons.length} aulas • ${DATA.questions.length} questões','${DATA.lessons.length} aulas • ${DATA.questions.length} questões • ${DATA.cards.length} cartões')
# Additional call to action above the homepage's first section: no layout overhaul
replace_once('function renderHome(){let next=', 'function renderHome(){let next=')
# Extend game setup
start=s.index('function startGame(mode)');end=s.index('function curQ()',start)
s=s[:start]+'''function pickGameQuestions(mode){
 let pool=[];
 if(mode==='focus'){
   pool=[...shuffle(DATA.questions.filter(q=>q.module==='Big Data')).slice(0,9),...shuffle(DATA.questions.filter(q=>q.module==='Raciocínio Lógico')).slice(0,6)];
 } else if(mode==='big'||mode==='logic'){
   pool=shuffle(DATA.questions.filter(q=>q.module===(mode==='big'?'Big Data':'Raciocínio Lógico'))).slice(0,15);
 } else if(mode==='adaptive'){
   const weak=new Set(Object.keys(state.mistakes).filter(id=>!(state.right[id] > (state.mistakes[id]?.count||0))));
   pool=[...shuffle(DATA.questions.filter(q=>weak.has(q.id))).slice(0,10)];
   let used=new Set(pool.map(q=>q.id));pool.push(...shuffle(DATA.questions.filter(q=>!used.has(q.id))).slice(0,15-pool.length));
 } else {
   const groups=[['Big Data',4],['Raciocínio Lógico',3],['Inteligência Artificial',2],['Business Intelligence',2],['Coleta de Dados',2],['Ciência de Dados',1],['Ética e Confiança',1]];
   groups.forEach(([module,n])=>pool.push(...shuffle(DATA.questions.filter(q=>q.module===module)).slice(0,n)));
 }
 // Apply a gentle difficulty curve while preserving some unpredictability in each tier.
 return pool.sort((a,b)=>a.difficulty-b.difficulty||Math.random()-.5);
}
function startGame(mode){
 let picked=pickGameQuestions(mode);
 state.game={mode,questions:picked.map(q=>{
   const options=shuffle(q.options.map((label,i)=>({label,originalIndex:i})));
   return {...q,options:options.map(i=>i.label),correct:options.findIndex(i=>i.originalIndex===q.correct)};
 }),stage:0,selected:null,status:'playing',used:{half:false,tip:false,skip:false,audience:false},hidden:[],tip:false,audience:null,earned:0};
 navigate('game');
}
''' + s[end:]
# add audience helper without overriding old help logic
start=s.index('function gameHelp(kind)');end=s.index('function renderGame()',start)
s=s[:start]+'''function gameHelp(kind){
 const g=state.game;if(!g||g.selected!==null||g.status!=='playing')return;const q=curQ();
 if(kind==='half'&&!g.used.half){g.hidden=shuffle([0,1,2,3].filter(i=>i!==q.correct)).slice(0,2);g.used.half=true}
 if(kind==='tip'&&!g.used.tip){g.tip=true;g.used.tip=true}
 if(kind==='audience'&&!g.used.audience){let pct=[0,0,0,0];pct[q.correct]=72;shuffle([0,1,2,3].filter(i=>i!==q.correct)).forEach((k,i)=>pct[k]=[12,9,7][i]);g.audience=pct;g.used.audience=true}
 if(kind==='skip'&&!g.used.skip&&g.stage<14){g.used.skip=true;g.stage++;g.hidden=[];g.tip=false;g.audience=null;g.selected=null}
 persist();render();
}
function stopGame(){
 const g=state.game;if(!g||g.status!=='playing'||g.selected!==null)return;
 g.status='stopped';g.earned=g.stage>0?prizes[g.stage-1]:0;
 state.games.push({date:Date.now(),stage:g.stage,prize:g.earned,mode:g.mode,stopped:true});persist();render();
}
''' + s[end:]
# modify landing text/action counts and options
replace_once('15 rodadas progressivas · 4 alternativas · 3 ajudas · explicações após respostas', '15 rodadas progressivas · 4 alternativas · 4 ajudas · opção de parar · explicações após respostas')
replace_once("${btn('Jogar: toda a matéria',`data-startgame=\"all\"`,'ghost')}", "${btn('Jogar: toda a matéria',`data-startgame=\"all\"`,'ghost')}${btn('Somente Big Data',`data-startgame=\"big\"`,'ghost')}${btn('Somente Bailly',`data-startgame=\"logic\"`,'ghost')}${btn('Treinar pontos fracos',`data-startgame=\"adaptive\"`,'ghost')}")
# improve game end screen
replace_once("let won=g.status==='won',n=g.stage;", "let won=g.status==='won',stopped=g.status==='stopped',n=g.stage;")
replace_once("${won?'DESAFIO COMPLETADO':'FIM DA RODADA'}", "${won?'DESAFIO COMPLETADO':stopped?'VOCÊ DECIDIU PARAR':'FIM DA RODADA'}")
replace_once("${won?'Você chegou ao milhão!':'Hora de revisar e tentar de novo'}", "${won?'Você chegou ao milhão!':stopped?'Você garantiu sua pontuação!':'Hora de revisar e tentar de novo'}")
replace_once("${fmtMoney(won?1000000:(n>=10?10000:n>=5?1000:0))}", "${fmtMoney(won?1000000:(stopped?g.earned:(n>=10?10000:n>=5?1000:0)))}")
replace_once("${g.mode==='focus'?'Big Data + Bailly':'Toda a matéria'}", "${({focus:'Big Data + Bailly',all:'Toda a matéria',big:'Somente Big Data',logic:'Somente Bailly',adaptive:'Treino adaptativo'})[g.mode]||'Estudo'}")
replace_once('<button class="lifeline" data-gamehelp="skip" ${g.used.skip||answered?\'disabled\':\'\'}>↪ Pular questão</button>', '<button class="lifeline" data-gamehelp="skip" ${g.used.skip||g.stage===14||answered?\'disabled\':\'\'}>↪ Pular questão</button><button class="lifeline" data-gamehelp="audience" ${g.used.audience||answered?\'disabled\':\'\'}>◉ Consultar plateia</button>')

# After help tip, show audience with an explicit simulation label.
needle='${answered?`<div class="feedback"><strong>${correct?'
assert needle in s
insert_audience = r'''${g.audience?`<div class="feedback"><strong>◉ Plateia simulada (fictícia, não são pessoas reais)</strong><div class="pollgrid">${g.audience.map((n,i)=>`<div><strong>${'ABCD'[i]} · ${n}%</strong><div class="bar"><span style="width:${n}%"></span></div></div>`).join('')}</div><p class="small" style="margin:8px 0 0">Estimativa ilustrativa da brincadeira, não garantia de acerto.</p></div>`:''}${!answered?`<div class="row" style="justify-content:flex-end;margin-top:14px">${btn('Parar e garantir pontuação',`data-action="game-stop"`,'ghost')}</div>`:''}'''
s=s.replace(needle,insert_audience+needle,1)
# Add a banner of practice on landing, before second home section
replace_once('<div class="sectionhead"><h2>Sua trilha de aprendizado</h2>', '<div class="sectionhead"><h2>Pratique para fixar</h2></div><div class="grid g3">${card(`<h3>▣ Treino adaptativo</h3><p class="small muted">Questões por assunto, revisão de erros e simulados sem gabarito antecipado.</p>${btn("Abrir treino →",`data-nav="practice"`,"primary")}`)}${card(`<h3>⚡ Casos reais</h3><p class="small muted">20 decisões sobre cenários de tecnologia e negócios.</p>${btn("Resolver missões →",`data-nav="cases"`,"soft")}`)}${card(`<h3>♛ Show do Milhão</h3><p class="small muted">Cinco modos, quatro ajudas e perguntas diferentes a cada partida.</p>${btn("Começar jogo →",`data-nav="game"`,"soft")}`)}</div><div class="sectionhead"><h2>Sua trilha de aprendizado</h2>')
# extend review export/import buttons and stats
replace_once('<div class="sectionhead"><h2>Caderno de erros</h2>', '<div class="sectionhead"><h2>Salve seu progresso</h2></div><div class="card"><p class="small muted">Seu progresso fica neste navegador. Exporte um backup para restaurar em outro navegador ou dispositivo. O JSON de estudo é separado do arquivo de progresso.</p><div class="row">${btn("Exportar progresso (.json)",`data-action="export-progress"`,"primary")}${btn("Importar progresso (.json)",`data-action="import-progress"`,"ghost")}</div><input type="file" id="progressFile" accept=".json,application/json" hidden></div><div class="sectionhead"><h2>Caderno de erros</h2>')
# extra JS block before showSource
insert=s.index('function showSource()')
ext=r'''// Treino com recuperação ativa, banco de erros e simulados sem gabarito instantâneo.
const quizAllModules='Todos';
function recordQuestion(q,correct){
 if(correct){state.right[q.id]=(state.right[q.id]||0)+1}
 else {state.mistakes[q.id]={count:(state.mistakes[q.id]?.count||0)+1,title:q.q,module:q.module,detail:q.explain}}
 persist();
}
function weightedTrainingPool(topic,diff,onlyWrong){
 const weak=new Set(Object.keys(state.mistakes));
 let arr=DATA.questions.filter(q=>(topic==='Todos'||q.module===topic)&&(!diff||q.difficulty===diff)&&(!onlyWrong||weak.has(q.id)));
 if(!arr.length)return [];
 return shuffle(arr).sort((a,b)=>{
  const xa=Number(state.mistakes[a.id]?.count||0) - Number(state.right[a.id]||0)*.35;
  const xb=Number(state.mistakes[b.id]?.count||0) - Number(state.right[b.id]||0)*.35;
  return xb-xa;
 });
}
function startTraining(kind){
 const topic=$('#topicFilter')?.value||'Todos',diff=Number($('#difficultyFilter')?.value||0),size=Number($('#sizeFilter')?.value||15);
 let pool=weightedTrainingPool(topic,diff,kind==='errors');
 if(!pool.length){alert('Não há questões para esse filtro. Teste outro assunto ou comece a responder para criar seu caderno de erros.');return}
 let selected=pool.slice(0,size);
 if(kind==='exam'){selected=shuffle(selected)}
 else {selected=selected.map(q=>q)}
 state.training={kind,questions:selected.map(q=>{
  const o=shuffle(q.options.map((text,index)=>({text,index})));
  return {...q,options:o.map(i=>i.text),correct:o.findIndex(i=>i.index===q.correct)};
 }),at:0,answers:[],selected:null,done:false,openedAt:Date.now(),topic};
 navigate('practice');
}
function chooseTrainingOption(i){
 const t=state.training;if(!t||t.done||t.selected!==null)return;
 t.selected=i;const q=t.questions[t.at];const right=i===q.correct;t.answers[t.at]={id:q.id,selected:i,correct:right};
 recordQuestion(q,right);
 render();
}
function nextTraining(){const t=state.training;if(!t||t.selected===null)return;t.at++;t.selected=null;if(t.at>=t.questions.length)t.done=true;render()}
function finishTraining(){if(!state.training)return;state.training.done=true;render()}
function quitTraining(){state.training=null;render()}
function renderPractice(){const t=state.training;
 if(!t)return `<div class="eyebrow">Treino de recuperação ativa</div><h1>Treine por assunto e faça simulados</h1><p class="muted">Escolha o tema, a dificuldade e o número de questões. No treino, a correção aparece após responder; no simulado, o gabarito completo só aparece ao terminar.</p>
 <div class="grid g3" style="margin-bottom:19px">${card(`<div class="label">Banco de questões</div><div class="statnum">${DATA.questions.length}</div><p class="small muted">Gabarito comentado e fonte</p>`)}${card(`<div class="label">Questões com erros</div><div class="statnum">${Object.keys(state.mistakes).length}</div><p class="small muted">Volte nelas até recuperar</p>`)}${card(`<div class="label">Casos reais</div><div class="statnum">${DATA.scenarios.length}</div><p class="small muted">Aplicação prática</p>`)}</div>
 <div class="card"><h2>Configure sua sessão</h2><div class="filters"><label>Assunto<select id="topicFilter" class="smart-select"><option value="Todos">Toda a matéria</option>${DATA.modules.map(m=>`<option value="${esc(m.id)}">${esc(m.label)}</option>`).join('')}</select></label><label>Dificuldade<select id="difficultyFilter" class="smart-select"><option value="0">Todos os níveis</option><option value="1">1 · Base</option><option value="2">2 · Aplicação</option><option value="3">3 · Pegadinhas</option></select></label><label>Quantidade<select id="sizeFilter" class="smart-select"><option value="10">10 questões</option><option value="15" selected>15 questões</option><option value="20">20 questões</option><option value="30">30 questões</option><option value="50">50 questões</option></select></label></div>
 <div class="row" style="margin-top:18px">${btn('Começar treino comentado',`data-training="practice"`,'primary')}${btn('Simulado sem respostas',`data-training="exam"`,'soft')}${btn('Revisar erros',`data-training="errors"`,'ghost')}</div></div>
 <div class="sectionhead"><h2>Como aproveitar melhor</h2></div><div class="grid g3">${card('<h3>1. Recuperar</h3><p class="small muted">Tente responder sem olhar resumos ou flashcards.</p>')}${card('<h3>2. Explicar</h3><p class="small muted">Confira o motivo do gabarito; não decore apenas a letra.</p>')}${card('<h3>3. Revisar</h3><p class="small muted">Refaça erros depois, com enunciados diferentes.</p>')}</div>`;
 if(t.done){let right=t.answers.filter(a=>a?.correct).length,percent=Math.round(100*right/t.questions.length);const incorrect=t.questions.map((q,i)=>({q,a:t.answers[i]})).filter(x=>x.a&&!x.a.correct);
 return `<div class="eyebrow">Resultado da sessão</div><div class="card"><h1>${percent}% de aproveitamento</h1><p class="muted">${right} acertos em ${t.questions.length} questões · equivalente a ${(10*right/t.questions.length).toFixed(1).replace('.',',')} / 10. Não é uma previsão da nota da prova.</p>${progress(percent)}<div class="row" style="margin-top:16px">${btn('Refazer treino',`data-action="quit-training"`,'primary')}${btn('Revisar flashcards',`data-nav="flash"`,'ghost')}</div></div><div class="sectionhead"><h2>Correção completa</h2></div><div class="grid" style="gap:12px">${t.questions.map((q,i)=>card(`<div class="row space"><strong>${i+1}. ${esc(q.q)}</strong><span class="pill ${t.answers[i]?.correct?'maxima':'baixa'}">${t.answers[i]?.correct?'✓ Acertou':'✕ Errou'}</span></div><p class="small muted" style="margin:10px 0 2px"><b>Sua resposta:</b> ${esc(t.answers[i]?.selected!=null?q.options[t.answers[i].selected]:'Não respondida')}</p><p class="small muted" style="margin:0 0 9px"><b>Resposta correta:</b> ${esc(q.options[q.correct])}</p><p class="small">${esc(q.explain)}</p><span class="label">${esc(q.source)}</span>`)).join('')}</div>`}
 const q=t.questions[t.at],answered=t.selected!==null;let prog=Math.round(100*t.at/t.questions.length);
 return `<div class="eyebrow">${t.kind==='exam'?'Simulado sem consulta':'Treino comentado'}</div><div class="row space"><h1>${t.kind==='exam'?'Simulado A1':'Treino de conceitos'}</h1><span class="pill">${t.at+1}/${t.questions.length}</span></div>${progress(prog)}<div class="card" style="margin-top:18px"><div class="row space"><span class="pill">${esc(q.module)}</span><span class="pill">Dificuldade ${q.difficulty}/3</span></div><h2 style="margin:18px 0 16px;font-size:22px">${esc(q.q)}</h2><div class="trainingchoices">${q.options.map((o,i)=>`<button class="choice ${answered&&t.kind!=='exam'&&i===q.correct?'correct':''} ${answered&&t.kind!=='exam'&&i===t.selected&&i!==q.correct?'wrong':''} ${answered&&i===t.selected?'selected':''}" data-traininganswer="${i}" ${answered?'disabled':''}><span class="letter">${'ABCD'[i]}</span>${esc(o)}</button>`).join('')}</div>${answered?`<div class="feedback"><strong>${t.kind==='exam'?'Resposta registrada. Gabarito ao final.':t.selected===q.correct?'✓ Resposta correta':'✕ Resposta incorreta'}</strong>${t.kind!=='exam'?`<p>${esc(q.explain)}</p><p class="small muted">Fonte: ${esc(q.source)}</p>`:''}<div class="row" style="margin-top:13px">${btn(t.at+1===t.questions.length?'Ver resultado':'Próxima pergunta →',`data-action="training-next"`,'primary')}</div></div>`:''}<div class="row" style="justify-content:flex-end;margin-top:14px">${btn('Encerrar sessão',`data-action="training-finish"`,'ghost')}</div></div>`;
}
function renderCases(){const scenes=DATA.scenarios,idx=state.casesIndex%scenes.length,c=scenes[idx],picked=state.casesSelected,chosen=picked!==null;
 const correctCount=Object.values(state.caseRight).reduce((a,b)=>a+b,0);
 return `<div class="eyebrow">Laboratório aplicado / Sem consulta</div><div class="row space"><h1>Missões práticas</h1><span class="pill">${idx+1} de ${scenes.length}</span></div><p class="muted">Você recebe uma situação semelhante ao mundo real e identifica o conceito que melhor explica o cenário. Os casos são didáticos, não itens oficiais da prova.</p>${progress(100*(idx)/scenes.length)}<div class="casepanel"><span class="eyebrow">Cenário ${String(idx+1).padStart(2,'0')} · ${esc(c.module)}</span><h2 style="font-size:26px;margin:10px 0 16px">${esc(c.title)}</h2><p style="font-size:17px;max-width:740px">${esc(c.story)}</p><span class="label">Qual conceito está em evidência?</span><div class="caseanswers">${c.choices.map((ch,i)=>`<button class="choice ${chosen&&i===c.correct?'correct':''} ${chosen&&picked===i&&i!==c.correct?'wrong':''}" data-caseanswer="${i}" ${chosen?'disabled':''}>${esc(ch)}</button>`).join('')}</div>${chosen?`<div class="feedback"><strong>${picked===c.correct?'✓ Boa interpretação!':'✕ Vamos revisar o foco do enunciado.'}</strong><p>${esc(c.explain)}</p><p class="small muted">Fonte conceitual: ${esc(c.source)}</p>${btn('Próxima missão →',`data-action="case-next"`,'primary')}</div>`:''}</div><div class="grid g2" style="margin-top:20px">${card(`<h3>Missões acertadas</h3><div class="statnum">${correctCount}</div><p class="small muted">O placar fica neste dispositivo.</p>`)}${card(`<h3>Aprender antes de testar</h3><p class="small muted">Aulas curtas sobre Vs e tipos de raciocínio.</p>${btn('Ver aulas →',`data-nav="learn"`,'soft')}`)}</div>`;
}
function answerCase(i){if(state.casesSelected!==null)return;const c=DATA.scenarios[state.casesIndex%DATA.scenarios.length];state.casesSelected=i;const counter=i===c.correct?state.caseRight:state.caseWrong;counter[c.id]=(counter[c.id]||0)+1;persist();render()}
function nextCase(){state.casesSelected=null;state.casesIndex=(state.casesIndex+1)%DATA.scenarios.length;render()}
function exportProgress(){let progressData={lastLesson:state.selectedLesson,done:state.done,cards:state.cards,mistakes:state.mistakes,right:state.right,games:state.games,caseRight:state.caseRight,caseWrong:state.caseWrong};try{progressData=JSON.parse(localStorage.getItem(key)||'{}')||progressData}catch(e){}const payload={app:'estudio-a1',version:2,exportedAt:new Date().toISOString(),progress:progressData};const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='estudio-a1-progresso.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1500)}
function importProgress(){const el=$('#progressFile');if(!el){navigate('review');setTimeout(importProgress,60);return}el.onchange=async()=>{const file=el.files?.[0];if(!file)return;try{const obj=JSON.parse(await file.text());if(obj.app!=='estudio-a1'||!obj.progress||typeof obj.progress!=='object')throw Error('Formato de backup incompatível');if(!confirm('Substituir o progresso atual pelo backup importado?'))return;localStorage.setItem(key,JSON.stringify(obj.progress));location.reload()}catch(err){alert('Não foi possível importar: '+err.message)}};el.click()}
'''
s=s[:insert]+ext+s[insert:]
# delegate events for new pages
replace_once('[data-startflash],[data-flashmark],[data-topic]', '[data-startflash],[data-flashmark],[data-topic],[data-training],[data-traininganswer],[data-caseanswer]')
replace_once('if(b.dataset.startgame){startGame(b.dataset.startgame);return}', 'if(b.dataset.startgame){startGame(b.dataset.startgame);return}if(b.dataset.training){startTraining(b.dataset.training);return}if("traininganswer" in b.dataset){chooseTrainingOption(+b.dataset.traininganswer);return}if("caseanswer" in b.dataset){answerCase(+b.dataset.caseanswer);return}')
replace_once("case'game-next':nextGameStage();break;", "case'game-next':nextGameStage();break;case'game-stop':stopGame();break;case'training-next':nextTraining();break;case'training-finish':finishTraining();break;case'quit-training':quitTraining();break;case'case-next':nextCase();break;case'export-progress':exportProgress();break;case'import-progress':importProgress();break;")
# cosmetics incl responsive
css='''
/* V2 interactive paths */
.smart-select{appearance:auto;background:#fff;color:#182238;border:1px solid #dce3f1;border-radius:11px;padding:12px 10px;font-size:13px;width:100%;margin-top:7px}
.filters{display:grid;grid-template-columns:2fr 1fr 1fr;gap:13px}
.filters label{font-size:12px;color:#647189;font-weight:800}
.trainingchoices{display:grid;gap:10px}.trainingchoices .choice{width:100%;text-align:left}
.casepanel{background:#fff;border-radius:22px;padding:30px;border:1px solid #e1e6f2;margin-top:17px;box-shadow:0 18px 50px #0b164010}
.caseanswers{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px}.caseanswers .choice{margin:0;width:100%;height:100%}
.pollgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-top:13px;font-size:11px;color:#dce8ff}.pollgrid .bar{margin-top:6px;height:7px}
.choice.selected:not(.correct):not(.wrong){outline:2px solid #8174ed}
@media(max-width:760px){.sectionhead{flex-wrap:wrap}.sectionhead>.pill{white-space:normal;max-width:100%}.filters{grid-template-columns:1fr}.caseanswers{grid-template-columns:1fr}.pollgrid{grid-template-columns:1fr 1fr}.casepanel{padding:20px}}
'''
replace_once('</style>',css+'</style>')
(root/'src/app_v2.template.html').write_text(s,encoding='utf-8')
print('Wrote V2 template',len(s))
