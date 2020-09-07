mkdir -p ~/.streamlit/
echo"\
[general]\n\
email=\"garavig.t@chula.ac.th\"\n\
">~/.streamlit/credentials/toml
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\