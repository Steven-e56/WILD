import os, shutil

out = "blip_finetuned_output"
# find the one checkpoint folder
ckpts = [d for d in os.listdir(out) if d.startswith("checkpoint")]
latest = sorted(ckpts, key=lambda x: os.path.getmtime(os.path.join(out, x)))[-1]
src_dir = os.path.join(out, latest)

# copy all files from the checkpoint into the root of blip_finetuned_output
for fn in os.listdir(src_dir):
    shutil.copy(os.path.join(src_dir, fn), out)
print("✓ Copied checkpoint files into", out)
