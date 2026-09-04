import os

html_content = """<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Saver AI</title>
    <style>
        :root {
            --primary-color: #0d6efd;
            --success-color: #198754;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #212529;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background-color: var(--card-bg);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            padding: 30px;
            width: 100%;
            max-width: 650px;
        }

        h2 {
            margin-top: 0;
            color: #0f172a;
            text-align: center;
            font-size: 24px;
        }

        p.subtitle {
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 14px;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.15);
        }

        textarea {
            height: 160px;
            resize: vertical;
        }

        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 14px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: #0b5ed7;
        }

        button:disabled {
            background-color: #94a3b8;
            cursor: not-allowed;
        }

        .status-box {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
            display: none;
        }

        .status-box.info {
            background-color: #e0f2fe;
            color: #0369a1;
            border: 1px solid #bae6fd;
            display: block;
        }

        .status-box.success {
            background-color: #d1e7dd;
            color: #0f5132;
            border: 1px solid #badbcc;
            display: block;
        }

        .status-box.error {
            background-color: #f8d7da;
            color: #842029;
            border: 1px solid #f5c2c7;
            display: block;
        }

        .instructions {
            background-color: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            font-size: 13px;
            color: #475569;
            margin-bottom: 20px;
            line-height: 1.5;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Contact Saver AI Web</h2>
    <p class="subtitle">Changanua na Uhifadhi Contacts Kiotomatiki</p>

    <div class="instructions">
        <b>Jinsi ya Kutumia:</b><br>
        1. Weka Mistral API Key yako hapa chini.<br>
        2. Bandika maelekezo au orodha ya majina na namba zote kwenye kisanduku.<br>
        3. Bonyeza kitufe cha **Kusanya na Kuhifadhi**.
    </div>

    <div class="form-group">
        <label for="apiKey">Mistral API Key:</label>
        <input type="text" id="apiKey" value="3pDTfrhKfqKtLyrKVwyMhC5A2xd7sv0C" placeholder="Ingiza API Key yako...">
    </div>

    <div class="form-group">
        <label for="rawText">Orodha ya Majina na Namba:</label>
        <textarea id="rawText" placeholder="Mfano:\n1. LC NJOMBE LUSY MSINA - 0617162589\n2. LC NJOMBE FATUMA JUMWA - 0626529573..."></textarea>
    </div>

    <button id="saveBtn" onclick="processContacts()">Hifadhi Kwenye Google Contacts</button>

    <div id="statusBox" class="status-box"></div>
</div>

<script>
async function processContacts() {
    const apiKey = document.getElementById('apiKey').value.trim();
    const rawText = document.getElementById('rawText').value.trim();
    const statusBox = document.getElementById('statusBox');
    const saveBtn = document.getElementById('saveBtn');

    if (!apiKey) {
        showStatus('Tafadhali ingiza Mistral API Key.', 'error');
        return;
    }

    if (!rawText) {
        showStatus('Tafadhali bandika majina na namba za simu.', 'error');
        return;
    }

    saveBtn.disabled = true;
    showStatus('AI inachanganua majina na namba... Tafadhali subiri.', 'info');

    try {
        // Step 1: Call Mistral API via Frontend Fetch
        const response = await fetch('https://api.mistral.ai/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'mistral-large-latest',
                messages: [
                    {
                        role: 'system',
                        content: "Wewe ni wasaidizi wa kuchanganua namba za simu na majina. Toa matokeo katika mfumo wa JSON pekee wenye orodha ya vitu vyenye 'name' na 'phone'. Format majina yawe 'LC [MKOA/MAHALI] [JINA]'. Format namba ziwe na kodi ya nchi (+255)."
                    },
                    {
                        role: 'user',
                        content: rawText
                    }
                ],
                temperature: 0.1
            })
        });

        const data = await response.json();

        if (response.ok && data.choices && data.choices.length > 0) {
            const content = data.choices[0].message.content;
            const jsonMatch = content.match(/\\[.*\\]/s);

            if (jsonMatch) {
                const contacts = JSON.parse(jsonMatch[0]);
                showStatus(`AI imefanikiwa kuchanganua Contacts ${contacts.length}! Tayari kwa kuhifadhi.`, 'success');
                console.log('Parsed Contacts:', contacts);
            } else {
                showStatus('AI imeshindwa kutenganisha majina na namba vizuri. Jaribu tena.', 'error');
            }
        } else {
            showStatus('Hitilafu kwenye API ya Mistral. Angalia API Key yako.', 'error');
        }

    } catch (err) {
        showStatus('Hitilafu ya mtandao: ' + err.message, 'error');
    } finally {
        saveBtn.disabled = false;
    }
}

function showStatus(message, type) {
    const statusBox = document.getElementById('statusBox');
    statusBox.innerText = message;
    statusBox.className = 'status-box ' + type;
}
</script>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html imetengenezwa kikamilifu!")