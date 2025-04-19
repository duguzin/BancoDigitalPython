//Função para enviar o Formulário de Login via AJAX
document.getElementById("login-form").addEventListener("submit", function(event) {
  event.preventDefault();

  //Obtém os Valores dos Campos de CPF e Senha
  const cpf = document.getElementById("cpf").value;
  const senha = document.getElementById("senha").value;

  const data = {
      cpf: cpf,
      senha: senha
  };

  //Envia uma Solicitação POST para o Backend (Flask) para realizar o Login
  fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          alert(data.message);

          if (data.message === "Login bem-sucedido!") {
              //Armazena os Dados do Usuário no LocalStorage
              localStorage.setItem('usuario', JSON.stringify(data));

              // Redireciona para o dashboard após login bem-sucedido
              window.location.href = "./dashboard.html";
          }
      }
  })
  .catch(error => console.error('Error:', error));
});
