mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"email@domain\"\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[theme]\n\
base = \"dark\"\
" > ~/.streamlit/config.toml