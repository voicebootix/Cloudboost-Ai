#!/usr/bin/env node
/**
 * Test script to verify frontend build process
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🧪 Testing Frontend Build Process');
console.log('================================');

// Check if package.json exists
const packageJsonPath = path.join(__dirname, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
  console.error('❌ package.json not found');
  process.exit(1);
}

// Read package.json
const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
console.log('✅ package.json found');

// Check for required dependencies
const requiredDeps = [
  '@radix-ui/react-slot',
  '@radix-ui/react-dialog',
  '@radix-ui/react-dropdown-menu',
  'react',
  'react-dom',
  'clsx',
  'tailwind-merge'
];

console.log('\n📦 Checking dependencies...');
const missingDeps = [];

requiredDeps.forEach(dep => {
  if (!packageJson.dependencies[dep]) {
    missingDeps.push(dep);
    console.log(`❌ Missing: ${dep}`);
  } else {
    console.log(`✅ Found: ${dep}@${packageJson.dependencies[dep]}`);
  }
});

if (missingDeps.length > 0) {
  console.log(`\n❌ Missing dependencies: ${missingDeps.join(', ')}`);
  process.exit(1);
}

// Check if node_modules exists
const nodeModulesPath = path.join(__dirname, 'node_modules');
if (!fs.existsSync(nodeModulesPath)) {
  console.log('\n📦 Installing dependencies...');
  try {
    execSync('npm install', { stdio: 'inherit', cwd: __dirname });
    console.log('✅ Dependencies installed');
  } catch (error) {
    console.error('❌ Failed to install dependencies');
    process.exit(1);
  }
} else {
  console.log('✅ node_modules found');
}

// Check if vite.config.js exists
const viteConfigPath = path.join(__dirname, 'vite.config.js');
if (!fs.existsSync(viteConfigPath)) {
  console.error('❌ vite.config.js not found');
  process.exit(1);
}
console.log('✅ vite.config.js found');

// Check if src directory exists
const srcPath = path.join(__dirname, 'src');
if (!fs.existsSync(srcPath)) {
  console.error('❌ src directory not found');
  process.exit(1);
}
console.log('✅ src directory found');

// Check if main App.jsx exists
const appPath = path.join(__dirname, 'src', 'App.jsx');
if (!fs.existsSync(appPath)) {
  console.error('❌ src/App.jsx not found');
  process.exit(1);
}
console.log('✅ src/App.jsx found');

// Check if components directory exists
const componentsPath = path.join(__dirname, 'src', 'components');
if (!fs.existsSync(componentsPath)) {
  console.error('❌ src/components directory not found');
  process.exit(1);
}
console.log('✅ src/components directory found');

console.log('\n🎉 All checks passed! The frontend should build successfully.');
console.log('\nTo test the build locally, run:');
console.log('  npm run build'); 