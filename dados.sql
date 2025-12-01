creat table clientes (
    nome varchar(50) not null,
    cpf char(11) unique not null,
    email varchar(50) unique not null,
    data_nascimento date,
    criado_em timestamp default current_timestamp
);
