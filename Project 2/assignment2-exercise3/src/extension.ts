import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    setSeasonalTheme();

    let disposable = vscode.commands.registerCommand('seasonal-themes', () => {
        vscode.window.showInformationMessage('Welcome to Seasonal Themes!');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}

export function setSeasonalTheme() {
    const currentSeason = getCurrentSeason();
    let themeName = '';
    switch (currentSeason) {
        case 'Autumn':
            themeName = 'Autumn Theme'; 
            break;
        case 'Winter':
            themeName = 'Winter Theme'; 
            break;
        case 'Spring':
            themeName = 'Spring Theme'; 
            break;
        case 'Summer':
            themeName = 'Summer Theme'; 
            break;
    }

    vscode.workspace.getConfiguration('workbench').update('colorTheme', themeName, true).then(
        () => {
            vscode.window.showInformationMessage(`Switched to the ${themeName}.`);
        },
        (err) => {
            console.error(`Error switching themes: ${err}`);
            vscode.window.showErrorMessage(`Error switching to the ${themeName} theme.`);
        }
    );
    
}


export function getCurrentSeason(): string {
    const month = new Date().getMonth();
    if (month >= 2 && month <= 4) {
        return 'Spring';
    } else if (month >= 5 && month <= 7) {
        return 'Summer';
    } else if (month >= 8 && month <= 10) {
        return 'Autumn';
    } else {
        return 'Winter';
    }
}