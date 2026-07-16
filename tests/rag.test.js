const test = require('node:test');
const assert = require('node:assert/strict');
const { chunkText, findRelevantChunks, buildEmbedding } = require('../server');

test('chunkText splits long text into overlapping chunks', () => {
    const text = 'One two three four five six seven eight nine ten eleven twelve.';
    const chunks = chunkText(text, 20, 5);
    assert.ok(chunks.length >= 2);
    assert.ok(chunks.every((chunk) => chunk.length > 0));
});

test('findRelevantChunks ranks the most relevant chunk first', () => {
    const chunks = [
        'The theory of relativity explains space and time.',
        'Photosynthesis converts sunlight into chemical energy.',
        'Machine learning models learn from examples.'
    ];
    const result = findRelevantChunks('What is relativity?', chunks, buildEmbedding);
    assert.equal(result[0].text, chunks[0]);
});
