mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
[theme]
base='light'
secondaryBackgroundColor='#eac5c5'
textColor='#000000'
\n\
" > ~/.streamlit/config.toml
