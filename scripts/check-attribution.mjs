import assert from 'node:assert/strict';
import { populateAttribution } from '../src/lib/attribution.js';

// A disabled CMS form supplies no inputs; it must not throw.
assert.doesNotThrow(() => populateAttribution({ querySelector: () => null }, '?utm_source=test'));
const names = ['utm_source', 'utm_medium', 'utm_campaign'];
const fields = Object.fromEntries(names.map(name => [name, { value: 'stale' }]));
const root = { querySelector: selector => fields[selector.match(/name="([^"]+)"/)[1]] };
populateAttribution(root, '?utm_source=newsletter&utm_medium=email&utm_campaign=EV%20launch&ignored=value');
assert.deepEqual(names.map(name => fields[name].value), ['newsletter', 'email', 'EV launch']);
populateAttribution(root, '');
assert.deepEqual(names.map(name => fields[name].value), ['', '', '']);
console.log('PASS: absent form, decoded campaign values, and missing parameters. Unit checks only; no submission sent.');
