---
name: bidxchange-change-workflow
description: Padroniza a implementação, correção, refatoração e entrega de alterações no repositório BidXchange, incluindo arquitetura Django, testes, validação local, branches, commits, pull requests e CI no GitHub. Use ao modificar arquivos do projeto; não use para perguntas conceituais ou inspeções estritamente somente leitura.
---

# Fluxo de alterações do BidXchange

Entregue alterações pequenas, verificáveis e coerentes com o domínio. Preserve o
trabalho existente do usuário e não transforme uma solicitação localizada em uma
reorganização ampla.

## 1. Estabelecer o escopo

Antes de editar:

1. Execute `git status --short --branch` e identifique mudanças preexistentes.
2. Leia os documentos relacionados, especialmente `docs/ARCHITECTURE.md`,
   `docs/DEVELOPMENT.md`, `PRODUCT.md`, `DESIGN.md` e `docs/FRONTEND.md` quando
   aplicáveis.
3. Traduza o pedido em comportamento esperado e critérios de aceite observáveis.
4. Classifique a mudança como `feat`, `fix`, `refactor`, `docs`, `test`,
   `chore` ou `perf` e identifique riscos de banco, autorização, interface,
   tempo real, configuração, dependências ou deploy.
5. Inspecione a implementação e os testes existentes antes de propor novos
   módulos ou abstrações.

Não sobrescreva mudanças preexistentes. Se houver sobreposição material com o
pedido, pare e explique o conflito.

## 2. Respeitar a arquitetura local

O BidXchange usa Django 6 server-rendered, com `accounts` para a experiência
pública e identidade e `bidxchange` para o produto autenticado.

- Coloque invariantes locais e persistência em `models/`.
- Coloque validação de entrada server-rendered em `forms/`.
- Coloque autorização de domínio em `policies/`.
- Coloque leituras complexas e reutilizáveis em `selectors/`.
- Coloque workflows transacionais e efeitos colaterais em `services/`.
- Mantenha `views/` focadas em HTTPS e escolha da resposta.
- Use `transaction.atomic()` para workflows de múltiplas escritas e
  `transaction.on_commit()` para efeitos que dependem do commit.
- Preserve labels dos apps, migrations, namespaces de URLs, templates e tabelas.
- Não edite `staticfiles/`; ele é saída de `collectstatic`.

Não crie outro app Django, mova módulos amplamente nem altere a identidade de app
sem aprovação explícita e um plano de migration.

## 3. Implementar com cobertura proporcional

Faça a menor mudança coesa que satisfaça os critérios a menos que o usuário mencione ser uma refatoração grande ou uma reformulação completa. Inclua ou
atualize testes no mesmo trabalho quando o comportamento mudar.

- **Models/banco:** gere a migration, inspecione as operações e teste invariantes,
  constraints e compatibilidade de dados. Nunca edite migrations já aplicadas.
- **Autorização/multitenancy:** teste acesso permitido, negado e cruzamento entre
  organizações. Validação somente na interface não é controle de acesso.
- **Services:** teste transação, estados inválidos e efeitos colaterais.
- **Views/forms:** teste método, autenticação, autorização, validação, redirect,
  template e mensagens relevantes.
- **Interface:** confira estados vazio, carregando, sucesso e erro; valide desktop
  e mobile e preserve acessibilidade e progressive enhancement. Use somente os
  namespaces `ui/`, `accounts/` e `bidxchange/`; não crie estilo inline, valor de
  paleta fora dos tokens nem cache-buster manual.
- **JavaScript/tempo real:** mantenha o servidor como fonte da verdade; teste
  isolamento dos grupos e publicação após commit.
- **Configuração/deploy:** atualize `.env.example` e a documentação sem incluir
  segredos; execute checks de produção quando houver ambiente seguro.

## 4. Validar em camadas

Durante a implementação, execute primeiro os testes diretamente relacionados:

```powershell
python "<skill-directory>/scripts/verify.py" --tests --test-label <label.do.teste>
```

Antes de entregar, execute o gate completo:

```powershell
python "<skill-directory>/scripts/verify.py" --all
```

Resolva `<skill-directory>` como a pasta pessoal que contém este `SKILL.md`.
Execute o script a partir da raiz do repositório BidXchange. A skill e seus
recursos pertencem ao Codex e nunca devem ser copiados, referenciados ou exigidos
pelo código, CI ou documentação do projeto.

O gate cobre integridade do diff, checks do Django, migrations pendentes,
`collectstatic` em dry-run, Stylelint, invariantes do frontend, Ruff, sintaxe
JavaScript e a suíte de testes. Não
declare que uma etapa passou se ela não foi executada. Se algo não puder rodar,
registre comando, causa e risco residual.

Para alterações visuais ou interativas, o gate automatizado não substitui uma
verificação real no navegador. Inspecione desktop em 1440 × 900 e mobile em
390 × 844 na mesma rodada, corrija os defeitos em lote e faça no máximo uma
rodada de confirmação.

## 5. Revisar antes de entregar

Revise `git diff --check`, `git diff --stat`, o diff completo e
`git status --short`. Confirme:

- o pedido e os critérios de aceite foram atendidos;
- não entraram segredos, `.env`, artefatos gerados ou mudanças alheias;
- migrations, documentação e `.env.example` acompanham o código quando aplicável;
- testes exercitam o risco principal, não somente o caminho feliz;
- textos da interface, documentação, commits e descrições de PR foram revisados
  quanto a ortografia, gramática, acentuação e principalmente clareza;
- a alteração segue as boas práticas do Django e as convenções documentadas do
  BidXchange, sem abstrações ou mudanças fora do escopo;
- não há logs de depuração, placeholders ou compatibilidade quebrada sem aviso.

## 6. Preparar Git e GitHub

Leia [references/github-workflow.md](references/github-workflow.md) ao criar ou
trocar branch, commitar, enviar, abrir uma pull request, acompanhar CI ou promover
uma versão. Essas ações alteram estado e exigem autorização compatível com o
pedido; implementar código não autoriza automaticamente commit, push, PR ou merge.
Nunca considere uma entrega ao GitHub concluída antes de confirmar que a alteração
chegou primeiro à `develop`, que a PR exigida foi preenchida e que todo o CI
obrigatório terminou sem erros.

Quando o pedido incluir commit, push e abertura de uma pull request, siga também
obrigatoriamente este checklist, nesta ordem:

1. Confirme que a alteração está em uma branch própria, diferente de `main` e
   `develop`, e que a branch foi criada ou atualizada a partir da versão mais
   recente possível de `develop`. Atualize referências remotas e, quando houver
   autorização para isso, atualize `develop` somente em fast-forward (`--ff-only`);
   não use stash,
   reset destrutivo, rebase ou force push para contornar conflitos.
2. Valide o nome da branch. Ele deve estar em português, todo em minúsculas,
   sem acentuação, e seguir exatamente:

   ```text
   tipo/nome/descricao-breve
   ```

   `tipo` deve usar Conventional Commits (`feat`, `fix`, `refactor`, `docs`,
   `test`, `chore` ou `perf`); `nome` identifica quem fez a alteração; e
   `descricao-breve` é uma descrição geral super curta. Use somente letras sem
   acento, números e hífens nos segmentos, sem espaços.
3. Antes de abrir a PR, confirme o diff, o commit e o estado da branch. Faça push
   somente com autorização compatível com o pedido.
4. Ao criar a PR no GitHub, use como base `develop`, preencha todas as informações
   exigidas por `bidxchange/.github/pull_request_template` (ou pelo caminho real
   equivalente encontrado no repositório), sem marcar validações não executadas.
5. Atribua a PR a si mesmo (`assign yourself`) e confirme que a atribuição foi
   aplicada.
6. Verifique os checks da PR e aguarde o CI obrigatório. Corrija ou reporte todo
   erro existente ou introduzido pela alteração; não declare a entrega concluída
   enquanto houver check obrigatório pendente ou com falha.

## Entrega obrigatória

Informe de forma concisa:

- comportamento entregue e decisões relevantes;
- arquivos ou áreas alteradas;
- comandos executados e seus resultados;
- migrations, configurações, riscos e validações manuais pendentes;
- estado Git e próximo passo no GitHub, sem afirmar push ou PR se não houve.
