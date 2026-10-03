/** Populate attribution only when the optional lead form exists. */
export function populateAttribution(root, search) {
  const params = new URLSearchParams(search);
  for (const name of ['utm_source', 'utm_medium', 'utm_campaign']) {
    const input = root.querySelector(`input[name="${name}"]`);
    if (input) input.value = params.get(name) || '';
  }
}
