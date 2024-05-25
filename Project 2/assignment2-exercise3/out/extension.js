"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCurrentSeason = exports.setSeasonalTheme = exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
function activate(context) {
    setSeasonalTheme();
    let disposable = vscode.commands.registerCommand('seasonal-themes', () => {
        vscode.window.showInformationMessage('Welcome to Seasonal Themes!');
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
function setSeasonalTheme() {
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
    vscode.workspace.getConfiguration('workbench').update('colorTheme', themeName, true).then(() => {
        vscode.window.showInformationMessage(`Switched to the ${themeName}.`);
    }, (err) => {
        console.error(`Error switching themes: ${err}`);
        vscode.window.showErrorMessage(`Error switching to the ${themeName} theme.`);
    });
}
exports.setSeasonalTheme = setSeasonalTheme;
function getCurrentSeason() {
    const month = new Date().getMonth();
    if (month >= 2 && month <= 4) {
        return 'Spring';
    }
    else if (month >= 5 && month <= 7) {
        return 'Summer';
    }
    else if (month >= 8 && month <= 10) {
        return 'Autumn';
    }
    else {
        return 'Winter';
    }
}
exports.getCurrentSeason = getCurrentSeason;
//# sourceMappingURL=extension.js.map