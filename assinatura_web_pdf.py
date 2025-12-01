import os
import shutil

# Caminho base
base_path = r'C:\Users\lwbs\Documents\PROJETOS\assinatura_web_pdf'

# Criar pasta
os.makedirs(base_path, exist_ok=True)
print(f"✓ Pasta criada: {base_path}")

# ============================================================
# 1. CRIAR index.html
# ============================================================

html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assinatura e Foto - PDF</title>
    <link rel="stylesheet" href="style.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>📋 Assinatura e Foto do Cliente</h1>
            <p class="subtitle">Capte assinatura, foto e gere PDF</p>
        </header>

        <main>
            <!-- Seção de Assinatura -->
            <section class="form-section">
                <h2>✍️ Assine abaixo:</h2>
                <canvas id="signature-pad" class="canvas-pad"></canvas>
                <div class="button-group">
                    <button id="clear-signature" class="btn btn-secondary">🗑️ Limpar Assinatura</button>
                </div>
            </section>

            <!-- Seção de Foto -->
            <section class="form-section">
                <h2>📷 Capturar Foto:</h2>
                <div class="video-container">
                    <video id="video" class="video-feed" autoplay></video>
                </div>
                <canvas id="photo-canvas" class="canvas-hidden"></canvas>
                <div class="button-group">
                    <button id="capture-photo" class="btn btn-primary">📸 Capturar Foto</button>
                </div>
                <div id="photo-preview" class="photo-preview hidden">
                    <p>Foto capturada:</p>
                    <img id="preview-img" alt="Preview">
                </div>
            </section>

            <!-- Seção de Ações -->
            <section class="form-section">
                <h2>💾 Salvar Dados:</h2>
                <div class="button-group">
                    <button id="download-data" class="btn btn-secondary">⬇️ Baixar Imagens</button>
                    <button id="save-pdf" class="btn btn-success">📄 Salvar como PDF</button>
                </div>
            </section>

            <!-- Status/Mensagens -->
            <div id="status-message" class="status-message hidden"></div>
        </main>

        <footer>
            <p>&copy; 2025 Sistema de Assinatura Digital</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>
'''

with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)
print("✓ Arquivo criado: index.html")

# ============================================================
# 2. CRIAR script.js
# ============================================================

js_content = '''// ============================================================
// SISTEMA DE ASSINATURA E FOTO COM GERAÇÃO DE PDF
// ============================================================

// ============================================================
// 1. INICIALIZAÇÃO E CONFIGURAÇÃO
// ============================================================

const canvas = document.getElementById('signature-pad');
const ctx = canvas.getContext('2d');
const video = document.getElementById('video');
const photoCanvas = document.getElementById('photo-canvas');
const photoCtx = photoCanvas.getContext('2d');
const statusMessage = document.getElementById('status-message');

let drawing = false;
let photoCapturada = false;

// ============================================================
// 2. FUNÇÕES UTILITÁRIAS
// ============================================================

function mostrarMensagem(texto, tipo = 'info') {
    statusMessage.textContent = texto;
    statusMessage.className = `status-message ${tipo}`;
    setTimeout(() => statusMessage.classList.add('hidden'), 4000);
}

function validarAssinatura() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    return imageData.some((pixel, index) => index % 4 === 3 && pixel > 128);
}

function validarFoto() {
    return photoCapturada;
}

// ============================================================
// 3. FUNCIONALIDADE DE ASSINATURA
// ============================================================

canvas.addEventListener('mousedown', () => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
});

canvas.addEventListener('mousemove', (event) => {
    if (!drawing) return;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#000';
    ctx.lineTo(event.offsetX, event.offsetY);
    ctx.stroke();
});

document.getElementById('clear-signature').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    mostrarMensagem('✓ Assinatura limpa', 'success');
});

// ============================================================
// 4. FUNCIONALIDADE DE CÂMERA
// ============================================================

navigator.mediaDevices.getUserMedia({ 
    video: { 
        width: { ideal: 400 }, 
        height: { ideal: 300 } 
    } 
})
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('Erro ao acessar câmera:', err);
        mostrarMensagem('❌ Erro: Câmera não disponível', 'error');
    });

document.getElementById('capture-photo').addEventListener('click', () => {
    photoCtx.drawImage(video, 0, 0, photoCanvas.width, photoCanvas.height);
    photoCapturada = true;
    
    const previewImg = document.getElementById('preview-img');
    previewImg.src = photoCanvas.toDataURL('image/png');
    document.getElementById('photo-preview').classList.remove('hidden');
    
    mostrarMensagem('✓ Foto capturada com sucesso', 'success');
});

// ============================================================
// 5. DOWNLOAD DE ARQUIVOS
// ============================================================

function downloadFile(filename, content) {
    const element = document.createElement('a');
    element.setAttribute('href', content);
    element.setAttribute('download', filename);
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

document.getElementById('download-data').addEventListener('click', () => {
    if (!validarAssinatura()) {
        mostrarMensagem('⚠️ Assinatura vazia. Assine antes de salvar.', 'warning');
        return;
    }
    if (!validarFoto()) {
        mostrarMensagem('⚠️ Foto não capturada. Capture uma foto primeiro.', 'warning');
        return;
    }

    const signatureData = canvas.toDataURL('image/png');
    const photoData = photoCanvas.toDataURL('image/png');
    const timestamp = new Date().toISOString().slice(0, 10);

    downloadFile(`assinatura_${timestamp}.png`, signatureData);
    downloadFile(`foto_${timestamp}.png`, photoData);
    
    mostrarMensagem('✓ Imagens baixadas com sucesso', 'success');
});

// ============================================================
// 6. GERAÇÃO DE PDF
// ============================================================

document.getElementById('save-pdf').addEventListener('click', () => {
    if (!validarAssinatura()) {
        mostrarMensagem('⚠️ Assinatura vazia. Assine antes de gerar PDF.', 'warning');
        return;
    }
    if (!validarFoto()) {
        mostrarMensagem('⚠️ Foto não capturada. Capture uma foto primeiro.', 'warning');
        return;
    }

    try {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });

        const timestamp = new Date().toLocaleString('pt-BR');
        
        // Título
        doc.setFontSize(18);
        doc.setTextColor(0, 51, 102);
        doc.text('DOCUMENTO ASSINADO DIGITALMENTE', 105, 20, { align: 'center' });

        // Data/Hora
        doc.setFontSize(10);
        doc.setTextColor(100, 100, 100);
        doc.text(`Gerado em: ${timestamp}`, 105, 28, { align: 'center' });

        // Linha separadora
        doc.setDrawColor(0, 51, 102);
        doc.line(10, 32, 200, 32);

        // Seção Assinatura
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);
        doc.text('ASSINATURA DO CLIENTE:', 10, 42);
        const signatureData = canvas.toDataURL('image/png');
        doc.addImage(signatureData, 'PNG', 10, 48, 80, 40);

        // Seção Foto
        doc.text('FOTO DO CLIENTE:', 110, 42);
        const photoData = photoCanvas.toDataURL('image/png');
        doc.addImage(photoData, 'PNG', 110, 48, 80, 60);

        // Rodapé
        doc.setFontSize(9);
        doc.setTextColor(150, 150, 150);
        doc.text('Este documento foi gerado automaticamente pelo sistema de assinatura digital.', 105, 285, { align: 'center' });

        const filename = `documento_assinado_${new Date().getTime()}.pdf`;
        doc.save(filename);
        
        mostrarMensagem(`✓ PDF "${filename}" gerado com sucesso`, 'success');
    } catch (error) {
        console.error('Erro ao gerar PDF:', error);
        mostrarMensagem('❌ Erro ao gerar PDF. Tente novamente.', 'error');
    }
});
'''

with open(os.path.join(base_path, 'script.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)
print("✓ Arquivo criado: script.js")

# ============================================================
# 3. COPIAR style.css (seu arquivo atual)
# ============================================================

style_source = r'C:\Users\lwbs\Documents\PROJETOS\style.css'
style_dest = os.path.join(base_path, 'style.css')

if os.path.exists(style_source):
    shutil.copy(style_source, style_dest)
    print("✓ Arquivo copiado: style.css")
else:
    print("⚠️ style.css não encontrado no caminho original, criando novo...")
    # Criar um novo se não existir
    with open(style_dest, 'w', encoding='utf-8') as f:
        f.write('''/* Estilos já configurados - veja o arquivo style.css copiado */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
''')

print("\n" + "="*60)
print("✅ PASTA CRIADA COM SUCESSO!")
print("="*60)
print(f"📁 Localização: {base_path}")
print("\n📂 Arquivos criados:")
print("   • index.html")
print("   • script.js")
print("   • style.css")
print("\n🚀 Para usar:")
print(f"   1. Abra: {base_path}\\index.html")
print("   2. Ou execute um servidor local (ex: python -m http.server)")
print("="*60)