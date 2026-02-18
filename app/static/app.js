const form = document.getElementById('generate-form');
const result = document.getElementById('result');
const statusText = document.getElementById('status');
const errorText = document.getElementById('error');
const video = document.getElementById('video');

async function pollJob(jobId) {
  while (true) {
    const res = await fetch(`/api/jobs/${jobId}`);
    const data = await res.json();
    statusText.textContent = `Status: ${data.status}`;
    if (data.status === 'succeeded') {
      video.src = data.output_url;
      video.classList.remove('hidden');
      return;
    }
    if (data.status === 'failed') {
      errorText.textContent = data.error || 'Generation failed';
      return;
    }
    await new Promise((r) => setTimeout(r, 1800));
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  result.classList.remove('hidden');
  video.classList.add('hidden');
  errorText.textContent = '';
  statusText.textContent = 'Submitting...';

  const payload = {
    prompt: document.getElementById('prompt').value,
    provider: document.getElementById('provider').value,
    model: document.getElementById('model').value,
    aspect_ratio: document.getElementById('aspect_ratio').value,
    duration_seconds: Number(document.getElementById('duration').value),
    negative_prompt: document.getElementById('negative_prompt').value || null,
  };

  const res = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json();
    statusText.textContent = '';
    errorText.textContent = err.detail || 'Failed to create job';
    return;
  }

  const job = await res.json();
  statusText.textContent = `Status: ${job.status}`;
  await pollJob(job.id);
});
