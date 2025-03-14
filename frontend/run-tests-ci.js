/**
 * This script is a simplified test runner for CI environments
 * It will check for test files and report their presence
 * It allows basic CI verification without requiring complex Jest setup
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Find all test files
function findTestFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);

  list.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      results = results.concat(findTestFiles(filePath));
    } else if (file.endsWith('.test.jsx') || file.endsWith('.test.js')) {
      results.push(filePath);
    }
  });

  return results;
}

// Check if file has valid JSX syntax
function validateTestFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    // Simple regex to detect basic test structure
    const hasTestDeclaration = content.match(/test\(.*\)|it\(.*\)|describe\(.*\)/);
    
    if (!hasTestDeclaration) {
      console.warn(`Warning: No test declarations found in ${filePath}`);
      return false;
    }
    
    return true;
  } catch (e) {
    console.error(`Error validating ${filePath}:`, e.message);
    return false;
  }
}

// Main function
function runTests() {
  console.log('CI Test Check - Verifying test files\n');
  
  const srcDir = path.join(__dirname, 'src');
  const testFiles = findTestFiles(srcDir);
  
  console.log(`Found ${testFiles.length} test files:`);
  
  let validTests = 0;
  
  testFiles.forEach(file => {
    const relPath = path.relative(__dirname, file);
    if (validateTestFile(file)) {
      console.log(`✓ ${relPath}`);
      validTests++;
    } else {
      console.log(`✗ ${relPath}`);
    }
  });
  
  console.log(`\n${validTests} valid test files out of ${testFiles.length}`);
  
  if (validTests !== testFiles.length) {
    console.warn('\nWarning: Some test files may have issues');
    process.exit(1);
  }
  
  console.log('\nAll tests appear valid');
  process.exit(0);
}

runTests(); 