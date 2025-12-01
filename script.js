// ...existing code...

// ============================================================
// 3. UPLOAD E CARREGAMENTO DE PDF (MODIFICADO)
// ============================================================

// Função para carregar PDF local automaticamente
function carregarDocumentoLocal() {
    // Tente diferentes nomes de arquivo
    const possiveisNomes = [
        'AUTORIZACAO DE PASSAGEM ENERGISA.pdf',
        'AUTORIZACAO_DE_PASSAGEM_ENERGISA.pdf',
        'autorizacao_de_passagem_energisa.pdf',
        'autorizacao de passagem energisa.pdf'
    ];

    // Tente carregar cada um
    possiveisNomes.forEach((nome, index) => {
        fetch(nome)
            .then(response => {
                if (response.ok) {
                    return response.arrayBuffer();
                }
                throw new Error(`Arquivo não encontrado: ${nome}`);
            })
            .then(data => {
                const typedArray = new Uint8Array(data);
                pdfjsLib.getDocument(typedArray).promise.then(pdf => {
                    pdfDoc = pdf;
                    currentPage = 1;
                    
                    document.getElementById('file-info').classList.remove('hidden');
                    document.getElementById('file-name').textContent = nome;
                    
                    document.getElementById('prev-page').disabled = false;
                    document.getElementById('next-page').disabled = false;
                    
                    signatureHistory = [];
                    renderPage(currentPage);
                    mostrarMensagem(`✓ Documento carregado: ${pdf.numPages} páginas`, 'success');
                }).catch(err => {
                    mostrarMensagem('❌ Erro ao carregar PDF', 'error');
                    console.error(err);
                });
            })
            .catch(err => {
                if (index === possiveisNomes.length - 1) {
                    mostrarMensagem('❌ Documento não encontrado na pasta', 'error');
                }
            });
    });
}

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files[0]) pdfUpload.files = files;
    handlePdfUpload();
});

// Clique para upload (agora é para trocar de documento)
uploadArea.querySelector('.link-upload').addEventListener('click', () => {
    pdfUpload.click();
});

pdfUpload.addEventListener('change', handlePdfUpload);

function handlePdfUpload() {
    const file = pdfUpload.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const typedArray = new Uint8Array(e.target.result);
        pdfjsLib.getDocument(typedArray).promise.then(pdf => {
            pdfDoc = pdf;
            currentPage = 1;
            
            document.getElementById('file-info').classList.remove('hidden');
            document.getElementById('file-name').textContent = file.name;
            
            document.getElementById('prev-page').disabled = false;
            document.getElementById('next-page').disabled = false;
            
            signatureHistory = [];
            renderPage(currentPage);
            mostrarMensagem(`✓ PDF carregado: ${pdf.numPages} páginas`, 'success');
        }).catch(err => {
            mostrarMensagem('❌ Erro ao carregar PDF', 'error');
            console.error(err);
        });
    };
    reader.readAsArrayBuffer(file);
}

// Carrega documento local quando a página abre
document.addEventListener('DOMContentLoaded', carregarDocumentoLocal);

// ...existing code...