import * as assert from 'assert';
import * as vscode from 'vscode';
import * as myExtension from '../extension';

suite('Extension Test Suite', () => {
	vscode.window.showInformationMessage('Start all tests.');

	test('Test getCurrentSeason', () => {
    const season = myExtension.getCurrentSeason();
    assert.ok(['Spring', 'Summer', 'Autumn', 'Winter'].includes(season), `Season should be one of the four seasons, got ${season}`);
});


	test('Test setSeasonalTheme', () => {
		myExtension.setSeasonalTheme();
	});

	test('Test command registration', async () => {
		const command = vscode.commands.getCommands(true).then(commands => {
			assert.ok(commands.includes('seasonal-themes'));
		});
	});
});
