import streamlit as st
import requests

API_URL = "http://localhost:5000"
LOGIN_URL = f"{API_URL}/auth/login"
USER_URL = f"{API_URL}/users"

st.set_page_config(page_title="API de Usuários", layout="centered")
st.title("🔐 Interface de Usuários - Flask + JWT")

# Sessão de autenticação
if "jwt" not in st.session_state:
    st.session_state.jwt = None

# Tela de login
if not st.session_state.jwt:
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        resp = requests.post(LOGIN_URL, json={"username": username, "password": password})
        if resp.status_code == 200:
            st.success("Login bem-sucedido!")
            st.session_state.jwt = resp.json()["access token"]
        else:
            st.error("Usuário ou senha inválidos.")

# Após login
else:
    st.success("Autenticado com sucesso!")
    headers = {
        "Authorization": f"Bearer {st.session_state.jwt}",
        "Content-Type": "application/json"
    }

    menu = st.sidebar.selectbox("Escolha a ação", ["Listar", "Criar", "Atualizar", "Deletar", "Logout"])

    if menu == "Listar":
        st.header("📋 Lista de Usuários")
        resp = requests.get(USER_URL, headers=headers)
        if resp.status_code == 200:
            users = resp.json()["Users"]
            st.json(users)
        else:
            st.error(f"Erro ao buscar usuários: {resp.text}")

    elif menu == "Criar":
        st.header("➕ Criar Usuário")
        uname = st.text_input("Novo nome de usuário")
        pwd = st.text_input("Senha", type="password")
        role_id = st.number_input("ID do Papel", min_value=1, step=1)

        if st.button("Criar"):
            payload = {"username": uname, "password": pwd, "role_id": role_id}
            resp = requests.post(USER_URL, headers=headers, json=payload)
            if resp.status_code == 201:
                st.success("Usuário criado com sucesso!")
            else:
                st.error(f"Erro ao criar usuário: {resp.text}")

    elif menu == "Atualizar":
        st.header("✏️ Atualizar Usuário")
        uid = st.number_input("ID do usuário a atualizar", min_value=1, step=1)
        new_name = st.text_input("Novo nome (opcional)")
        new_pwd = st.text_input("Nova senha (opcional)", type="password")
        active = st.selectbox("Ativo?", [True, False])

        if st.button("Atualizar"):
            data = {"active": active}
            if new_name:
                data["username"] = new_name
            if new_pwd:
                data["password"] = new_pwd
            resp = requests.patch(f"{USER_URL}/{uid}", headers=headers, json=data)
            if resp.status_code == 200:
                st.success("Usuário atualizado!")
                st.json(resp.json())
            else:
                st.error(f"Erro: {resp.text}")

    elif menu == "Deletar":
        st.header("🗑️ Deletar Usuário")
        uid = st.number_input("ID do usuário a deletar", min_value=1, step=1)
        if st.button("Deletar"):
            resp = requests.delete(f"{USER_URL}/{uid}", headers=headers)
            if resp.status_code == 204:
                st.success("Usuário deletado com sucesso!")
            else:
                st.error(f"Erro ao deletar: {resp.text}")

    elif menu == "Logout":
        st.session_state.jwt = None
        st.experimental_rerun()
