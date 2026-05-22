async function pagar() {

    const nome =
        document.getElementById(
            "nome"
        ).value;
    const valor =
        Number(
            document.getElementById(
                "valor"
            ).value
        );

    const resposta = await fetch(
        "http://127.0.0.1:5000/pagamento",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                nome: nome,
                valor: valor
            })
        }
    );
    const dados =
        await resposta.json();

    window.location.href =
        dados.checkout_url;
}