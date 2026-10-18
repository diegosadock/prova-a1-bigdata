# Estúdio A1 v2 — Análise de Dados e Big Data

Plataforma de revisão construída sobre as quatro apostilas fornecidas: Aula 1 (89 slides), Aula 2 (45), Aula 3 (31) e Aula 5 do professor Bailly (17). Total: 182 slides.

## O que está incluído

- 34 aulas, com sínteses dos conceitos apresentados nos slides, analogias, exemplos didáticos e mini-desafios;
- 150 questões de múltipla escolha com respostas e correção conceitual;
- 20 missões práticas para identificar os 5 Vs e os cinco tipos de raciocínio;
- 138 flashcards com revisão simplificada e seleção de cartas vencidas/difíceis;
- Quiz estilo **Show do Milhão**, com 15 etapas, 5 modos de jogo, eliminar 2, dica, plateia **fictícia**, pular e parar (pular não funciona na última pergunta);
- Treinos por tema, nível, 10–50 questões, revisão dos erros e simulados com gabarito apenas no final;
- Caderno de erros, desempenho, salvamento local e exportação/importação do progresso em JSON.

**Aviso pedagógico:** as questões não são oficiais; muitas são exemplos e situações didáticas inspiradas nos conceitos dos PDFs. Os slides listam **cinco Vs**, e não confirmam um sexto V. Os conteúdos relacionados a Power BI e proteção de dados têm prioridade de revisão menor, conforme mensagem informal compartilhada pelo estudante.

## Publicar no Cloudflare Workers (modo estático)

Na raiz deste pacote estão `wrangler.jsonc`, `public/`, `src/` e `scripts/`.

1. Envie o conteúdo do pacote para a raiz de seu repositório GitHub.
2. Em Cloudflare Workers & Pages, conecte o repositório usando **Workers Builds**.
3. `Root directory`: raiz do repositório; `Build command`: vazio; `Deploy command`: `npx wrangler deploy`.
4. O Wrangler usa o `wrangler.jsonc` para publicar `./public` sem backend nem bundler.
5. Para Cloudflare Pages em vez de Workers: `Build command`: `exit 0`; `Build output directory`: `public`.

Os arquivos já estão compilados em `public/`: **não é preciso instalar Python, Node ou bibliotecas para o deploy automático** (o Wrangler pode ser instalado automaticamente na etapa de deploy).

## Banco de conteúdos em JSON

Edite **`src/conteudo.json`**, que é a fonte dos dados didáticos. As chaves principais são:

```json
{
  "lessons": [],
  "modules": [],
  "questions": [],
  "cards": [],
  "scenarios": [],
  "metadata": {}
}
```

### Exemplo de questão

```json
{
  "id": "nova-questao-01",
  "module": "Big Data",
  "q": "Uma plataforma recebe imagens, vídeos e arquivos JSON. Qual V é destacado?",
  "options": ["Valor", "Variedade", "Volume", "Veracidade"],
  "correct": 1,
  "explain": "O enunciado destaca a diversidade de formatos e estruturas dos dados.",
  "source": "Aula 1 · p. 9 (exemplo didático)",
  "difficulty": 2
}
```

`correct` começa em **0**: no exemplo acima, o índice 1 é a segunda alternativa.

Após editar `src/conteudo.json`, gere os arquivos públicos com:

```bash
python scripts/build.py
```

Faça commit tanto do `src/conteudo.json` quanto dos arquivos gerados `public/index.html` e `public/data/conteudo.json`. O arquivo HTML carrega os dados do JSON **embutidos pelo gerador** para funcionar até quando aberto diretamente como arquivo local, sem precisar de `fetch` remoto. `public/data/conteudo.json` é a cópia legível do banco de conteúdo, mas a edição precisa passar pelo gerador para sincronizar a aplicação.

> Não execute `expand_content.py` para editar uma questão isolada. Ele serve para reproduzir o conjunto de expansão original, usando `src/conteudo_base.json` e seu banco de questões fixo; poderia sobrescrever modificações manuais. Para manutenção normal, edite `src/conteudo.json` e execute apenas `build.py`.

## Armazenamento dos resultados

O progresso é guardado no `localStorage` do navegador, sem servidor. Para levá-lo a outro navegador ou computador, abra `Meu desempenho` → `Exportar progresso` e depois `Importar progresso` no navegador de destino. Os dados **não são sincronizados automaticamente** entre dispositivos. O arquivo de backup é diferente do banco de conteúdo público.

## Tutoria inteligente (limite da versão estática)

Os botões "Não entendi — explica mais simples" e "Exemplo por analogia" apresentam **alternativas já cadastradas no conteúdo**. "Perguntar ao ChatGPT" copia um prompt contextualizado para abrir nesta conversa; **não existe IA generativa conectada ao site**. Para perguntas de acompanhamento geradas dinamicamente pelo modelo, seria necessário um backend com API, autenticação e proteção de chave, não apenas JSON estático.

## Requisitos

HTML, CSS e JS sem dependências de execução. Deploy compatível com Cloudflare Workers Static Assets ou Cloudflare Pages. Scripts de manutenção exigem Python 3 instalado localmente.
