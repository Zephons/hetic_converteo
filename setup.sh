mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[theme]\n\
primaryColor = 'purple'\n
" > ~/.streamlit/config.toml