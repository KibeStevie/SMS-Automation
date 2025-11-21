# 📱SMS Notification System via Microsoft Phone Link
<em>Automated SMS Delivery Using Windows UI Automation</em>
<strong>Note:</strong> This project interacts with Microsoft Phone Link via UI automation — <strong>not</strong> through any official API. It simulates human interaction with the app’s interface. Use responsibly and in compliance with local messaging regulations.

## ✅ Overview
This Python script automates sending personalized SMS messages to a list of phone numbers using <strong>Microsoft Phone Link</strong> on Windows. It provides <strong>two implementation approaches</strong>:
<table>
  <tr>
    <th>Approach</th>
    <th>Method</th>
    <th>Reliability</th>
    <th>Best For</th>
  </tr>
  <tr>
    <td><strong>1. Hardcoded Coordinates</strong></td>
    <td>Uses fixed screen positions (<code>pyautogui.click(x, y)</code>)</td>
    <td>⚠️ Low — breaks with screen scaling/UI changes</td>
    <td>Quick testing, single-device use</td>
  </tr>
  <tr>
    <td><strong>2. Screenshot-Based</strong></td>
    <td>Uses image recognition (<code>pyautogui.locateOnScreen()</code>)</td>
    <td>✅ High — works across resolutions and minor UI changes</td>
    <td>Production use, portability, reliability</td>
  </tr>
</table>
Both approaches read phone numbers from <code>contacts.csv</code>, send a predefined message via Phone Link, and log results to <code>logs/sms_log.txt</code>.

## 🛠️ Prerequisites
<h3>✅ Software Requirements</h3>
<ul>
  <li><strong>Windows 10/11</strong> (Phone Link requires Windows)</li>
  <li><strong>Microsoft Phone Link</strong> installed and connected to your Android device</li>
  <li><strong>Python 3.9+</strong></li>
</ul>

## 📁 Project Structure</h2>
  <pre>
SMS-Automation/
│
├── sms_sender_1.py               # Main script (supports both approaches)
├── contacts.csv                  # CSV file with phone numbers (one per row)
├── logs/                         # Auto-generated log file (sms_log.txt)
├── screenshots/                  # Folder for UI element images (Screenshot approach only)
│   ├── new_message_button.png
│   ├── phone_number_input.png
│   └── message_input.png
│
└── README.html                   # This file
  </pre>
  ✅ <strong>Create the folders <code>logs/</code> and <code>screenshots/</code> before running the script.</strong>

## 📄 File Formats</h2>
### 1. <code>contacts.csv</code>
Format: One phone number per row.
<pre>0704581833
0712345678
0798765432</pre>

❗ Ensure numbers are <strong>numeric only</strong> (no spaces, +, or dashes). The script will skip invalid entries and log them.

### 2. Screenshots (Screenshot Approach Only)
Take <strong>clear, high-contrast screenshots</strong> of these elements in Microsoft Phone Link:

<table>
  <tr>
    <th>Element</th>
    <th>Screenshot Name</th>
    <th>How to Capture</th>
  </tr>
  <tr>
    <td><strong>New Message Button</strong></td>
    <td><code>new_message_button.png</code></td>
    <td>Click the “+” or “New Message” button in Phone Link</td>
  </tr>
  <tr>
    <td><strong>Message Input Field</strong></td>
    <td><code>message_input.png</code></td>
    <td>Click inside the message text box — capture the typing area</td>
  </tr>
</table>

🔍 <strong>Tips for better recognition:</strong>
<ul>
  <li>Use <strong>100% zoom</strong> in Phone Link</li>
  <li>Avoid shadows, transparency, or blurred edges</li>
  <li>Save as <strong>PNG</strong> (not JPG)</li>
  <li>Match the <strong>exact name</strong> in the code</li>
</ul>

## ▶️ Setup & Run Instructions</h2>
<h3>✅ Step 1: Prepare Your Environment</h3>
<h3> 2. 📦 Python Dependencies</h3>
Install required packages:

```bash
python -m venv venv
source ./venv/Scripts/ativate
python install -r requirements.txt
```

<h3>✅ Step 2: Customize the Message</h3>
Open <code>sms_sender_1.py</code> and change the message:
<pre>MESSAGE = "Hello! This is an automated test message."</pre>

<h3>✅ Step 3: Choose Your Approach</h3>
<h4>🔧 Approach 1: Hardcoded Coordinates (Quick Start)</h4>
Use this if you just want to test quickly on your current screen. No setup needed beyond <code>contacts.csv</code>. The script uses fixed coordinates — <strong>only works on your exact screen setup</strong>.
<pre>python sms_sender.py</pre>

<h4>🖼️ Approach 2: Screenshot-Based (Recommended)</h4>
Use this for reliability across devices and future-proofing.
<ul>
  <li>Ensure your <code>screenshots/</code> folder contains:
    <ul>
      <li><code>new_message_button.png</code></li>
      <li><code>phone_number_input.png</code></li>
      <li><code>message_input.png</code></li>
    </ul>
  </li>
  <li>Run the script:</li>
</ul>
<pre>python sms_sender_1.py</pre>

💡 The script will <strong>automatically detect</strong> which approach to use based on whether the screenshot files exist.

## ⚙️ How It Works</h2>
### Main Workflow:
<ol>
<li>Script reads <code>contacts.csv</code></li>
<li>Waits 3 seconds for you to open and focus <strong>Microsoft Phone Link</strong></li>
<li>For each number:</li>
<ul>
  <li>Clicks the “New Message” button (via coordinates or screenshot)</li>
  <li>Types the phone number → presses Enter</li>
  <li>Clicks the message input field → types message → presses Enter</li>
  <li>Logs result to <code>logs/sms_log.txt</code></li>
</ul>
</ol>

### Logging
All attempts are recorded in <code>logs/sms_log.txt</code>:
<pre>[2025-11-22 14:30:25] SUCCESS - 0704581833
[2025-11-22 14:31:10] FAILED - 0712345678 (Could not find phone_number_input after 10 seconds)
[2025-11-22 14:32:05] FAILED - 123abc (Invalid number)</pre>

## 🚨 Important Notes & Limitations</h2>
<table>
  <tr>
    <th>Consideration</th>
    <th>Detail</th>
  </tr>
  <tr>
    <td><strong>No API</strong></td>
    <td>This uses UI automation — not a supported or secure method. Use for personal automation only.</td>
  </tr>
  <tr>
    <td><strong>Phone Link Must Be Active</strong></td>
    <td>The Phone Link window must be <strong>visible, focused, and unlocked</strong> on your desktop.</td>
  </tr>
  <tr>
    <td><strong>Screen Resolution Matters</strong></td>
    <td>Hardcoded coordinates break if you change resolution or scale. Screenshot approach is resilient.</td>
  </tr>
  <tr>
    <td><strong>Speed Limit</strong></td>
    <td>3-second delay between messages prevents spam detection. Do not reduce below 2s.</td>
  </tr>
  <tr>
    <td><strong>Android Sync Required</strong></td>
    <td>Your phone must be connected to Phone Link and SMS enabled.</td>
  </tr>
  <tr>
    <td><strong>Ethics & Compliance</strong></td>
    <td>Do not send unsolicited messages. Respect privacy and local laws (e.g., TCPA, GDPR).</td>
  </tr>
</table>

## 🛠️ Troubleshooting
<table>
<tr>
  <th>Issue</th>
  <th>Solution</th>
</tr>
<tr>
  <td><code>Could not find [element] after 10 seconds</code></td>
  <td>Take a new screenshot of the missing UI element. Ensure it’s in <code>screenshots/</code> with the correct name.</td>
</tr>
<tr>
  <td>Script does nothing</td>
  <td>Make sure Phone Link is open, focused, and visible on your primary monitor.</td>
</tr>
<tr>
  <td>Message sent twice</td>
  <td>You may have clicked manually while script was running. Close other inputs.</td>
</tr>
<tr>
  <td><code>Image not found</code> error</td>
  <td>Check spelling of screenshot filenames. They must match exactly: <code>new_message_button.png</code> (not <code>NewMessage.png</code>)</td>
</tr>
<tr>
  <td><code>The confidence keyword argument is only available if OpenCV is installed</code></td>
  <td>Install OpenCV: <code>pip install opencv-python</code> — or remove <code>confidence=</code> parameter from <code>locateOnScreen()</code></td>
</tr>
</table>

## 💡 Pro Tips</h2>
<div class="tip">
  <ul>
    <li>✅ Test first: Run the script with <strong>one number</strong> before bulk sending.</li>
    <li>✅ Use <strong>Screenshot Approach</strong> for any serious or repeated use.</li>
    <li>✅ Run in <strong>full-screen mode</strong> on a 1920x1080 or higher display for best results.</li>
    <li>✅ Always check <strong>logs</strong> — they tell you exactly what failed and why.</li>
    <li>✅ <strong>Backup your screenshots</strong> — if you update Windows or Phone Link, re-capture them.</li>
  </ul>
</div>

## 📌 Final Notes</h2>
This project demonstrates how to <strong>automate tasks on applications without APIs</strong> — a valuable skill in legacy system integration, QA automation, and accessibility tooling.

