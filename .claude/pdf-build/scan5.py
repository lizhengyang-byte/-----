import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
p = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'native', '01-土的物理性质与分类.md'],
                   capture_output=True, encoding='utf-8')
out = p.stdout
idx = out.find('31890\47')
print('---- region around 粒径 (native) ----')
if idx >= 0:
    print(out[max(0, idx-400):idx+600])
else:
    # fallback: search for "60"
    i = out.find('60')
    print('fallback, first 60 at', i)
    print(out[max(0, i-200):i+400])
