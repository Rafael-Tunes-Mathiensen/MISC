# Fluxo Git e GitHub

Leia esta referência somente quando a tarefa envolver github, branch, commit, push,
pull request, CI, revisão ou promoção para produção.

## Modelo de branches

- `main` representa produção. Nunca faça commit ou push direto nela.
- `develop` é a linha de integração. Trabalho novo parte da versão atualizada de
  `develop` e retorna por pull request.
- Use uma branch própria por mudança, seguindo exatamente o padrão em português,
  sem acentuação e todo em minúsculas:
  `tipo/nome/descricao-breve`.
- Em `tipo`, use `feat`, `fix`, `refactor`, `docs`, `test`, `chore` ou `perf`.
  Em `nome`, identifique quem fez a alteração. Em `descricao-breve`, use uma
  descrição geral super curta. Use somente letras sem acento, números e hífens
  nos segmentos, sem espaços.
- Uma release é promovida exclusivamente por PR de `develop` para `main`.

Toda mudança destinada ao GitHub deve chegar primeiro à `develop`. Nunca envie uma
branch de trabalho diretamente à `main`. Antes do push, determine o caminho:

- se a mudança está em uma branch de trabalho, a PR para `develop` é obrigatória;
- se a mudança já está em `develop`, confirme que ela foi integrada pelo fluxo
  aprovado e não crie uma PR redundante;
- se a proteção do repositório ou o histórico não permitirem comprovar o fluxo,
  prefira criar uma branch e uma PR para `develop`.

Antes de criar ou usar uma branch, confirme que o worktree está limpo ou que
mudanças existentes pertencem ao mesmo trabalho. Atualize as referências remotas
e mantenha `develop` o mais atualizada possível; atualize a branch local com
`git pull --ff-only` somente quando essa mutação estiver autorizada. Confirme que
a branch de trabalho está baseada na versão atualizada de `develop`. Nunca
esconda trabalho com stash, reset, checkout destrutivo ou rebase sem autorização.

## Commits

Use Conventional Commits com um assunto curto e imperativo:

```text
<tipo>: <descrição em português>
```

Tipos aceitos: `feat`, `fix`, `refactor`, `docs`, `test`, `chore` e
`perf`. Evite misturar refatorações independentes ou arquivos não relacionados.
Antes do commit, revise exatamente o que será incluído com `git diff --staged`.
Revise também a ortografia e a acentuação da mensagem, preservando nomes técnicos,
identificadores e termos que o projeto deliberadamente mantém em inglês.

Não crie commit, não faça push e não reescreva histórico sem autorização do
usuário. Nunca use `--force` como passo rotineiro.

## Pull requests

Branches de trabalho abrem PR para `develop`. Apenas a PR de release usa
`main` como base e `develop` como head.

Preencha `.github/pull_request_template.md` com informação concreta:

- título no padrão Conventional Commits;
- descrição geral, e análise dos checkbox, que se corretos e atendidos marcar com o [x];
- decisões técnicas e arquivos centrais;
- comandos realmente executados e resultados;
- impacto em banco, compatibilidade, variáveis e deploy;
- plano de reversão proporcional;
- evidência visual ou operacional quando aplicável.

Ao abrir a PR, use `develop` como base, preencha todos os campos do template real
do repositório, atribua a PR a si mesmo (`assign yourself`) e confirme que a
atribuição foi aplicada. Se o template estiver em
`bidxchange/.github/pull_request_template`, use esse arquivo; caso o layout do
repositório seja diferente, localize o caminho equivalente antes de preencher a
PR.

Não marque checkboxes de validações não executadas. Aguarde o job obrigatório
`Django CI / test` em todas as versões de Python e trate falhas antes do merge.
Revise todo o questionário da PR, incluindo ortografia, acentuação e coerência com
o diff. Não conclua a entrega ao GitHub enquanto algum check obrigatório estiver
pendente ou com erro.
Se a falha não puder ser resolvida no escopo autorizado,
informe o bloqueio e o risco residual em vez de declarar a alteração concluída
A menos que o erro for no Vercel e o usuário que está fazendo as alterações não for o Rafael Tunes Mathiensen,
Nesse caso apenas marque como alteração concluída porem por falta de permissão não lançada na Vercel.

## Proteção da main e versão estável

Antes de qualquer ação que envolva a `main`, pergunte explicitamente ao usuário
se ele realmente deseja executar essa ação e se autoriza publicar uma versão
estável do projeto. Essa confirmação deve ocorrer imediatamente antes da ação e
não pode ser inferida de uma autorização anterior para implementar, commitar,
enviar à `develop` ou abrir outra PR.

Isso inclui trocar para ou atualizar `main`, criar uma PR direcionada a ela,
fazer merge, commit, push, tag, release ou iniciar o deploy de produção. Sem a
confirmação explícita, pare com a alteração validada em `develop` e apresente o
próximo passo proposto.

Se um cliente GitHub autenticado não estiver disponível, não improvise tokens:
entregue a branch pronta e os passos manuais necessários.

## Proteções recomendadas no GitHub

Configure nas regras do repositório:

- `main`: exigir PR, aprovação do CODEOWNER, CI verde, conversas resolvidas,
  bloquear force push e deleção; permitir somente PR vinda de `develop`.
- `develop`: exigir PR, CI verde e conversas resolvidas; bloquear force push e
  deleção.
- exigir que a branch esteja atualizada antes do merge quando o custo do novo CI
  for aceitável;
- habilitar exclusão automática da branch após o merge.

As proteções remotas não são alteradas sem autorização explícita. Confirme os
nomes reais dos status checks na interface antes de torná-los obrigatórios.

## Critério de conclusão

Uma alteração está pronta para merge quando tem escopo único, critérios de aceite
atendidos, diff revisado, gate local completo ou impedimentos documentados, PR
preenchida, revisão concluída e CI obrigatório verde. Merge e deploy continuam
sendo ações separadas e explicitamente autorizadas.
