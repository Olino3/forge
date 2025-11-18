#!/usr/bin/env ts-node
/**
 * Angular Test Analyzer Helper Script
 *
 * This script helps analyze existing Angular test files to understand:
 * - Testing framework used (Jest vs Jasmine/Karma)
 * - Test file naming conventions
 * - TestBed configuration patterns
 * - Mock creation patterns
 * - Common test structures
 *
 * Usage:
 *     ts-node test_analyzer.ts <test_directory>
 *     ts-node test_analyzer.ts <test_file.spec.ts>
 */

import * as fs from 'fs';
import * as path from 'path';

interface TestAnalysis {
  file: string;
  framework: 'jest' | 'jasmine' | 'unknown';
  testCount: number;
  usesTestBed: boolean;
  usesHttpMocking: boolean;
  usesMockStore: boolean;
  describeBlocks: string[];
  mockPatterns: string[];
  angularVersion?: string;
}

interface AggregateAnalysis {
  testFilesCount: number;
  totalTests: number;
  primaryFramework: 'jest' | 'jasmine' | 'mixed';
  frameworkCounts: { jest: number; jasmine: number };
  testBedUsage: string;
  httpMockingPattern: string;
  ngrxUsage: string;
  testFiles: string[];
  namingPattern: string;
  commonPatterns: string[];
}

function analyzeTestFile(filePath: string): TestAnalysis {
  const content = fs.readFileSync(filePath, 'utf-8');

  return {
    file: filePath,
    framework: detectFramework(content),
    testCount: countTests(content),
    usesTestBed: content.includes('TestBed.configureTestingModule'),
    usesHttpMocking: detectHttpMocking(content),
    usesMockStore: content.includes('provideMockStore') || content.includes('MockStore'),
    describeBlocks: findDescribeBlocks(content),
    mockPatterns: findMockPatterns(content),
    angularVersion: detectAngularVersion(content),
  };
}

function detectFramework(content: string): 'jest' | 'jasmine' | 'unknown' {
  const hasJest =
    content.includes('jest.fn()') ||
    content.includes('jest.mock') ||
    content.includes('jest.spyOn') ||
    content.includes('mockReturnValue');

  const hasJasmine =
    content.includes('jasmine.createSpyObj') ||
    content.includes('spyOn(') ||
    content.includes('.and.returnValue') ||
    content.includes('HttpTestingController');

  if (hasJest && !hasJasmine) return 'jest';
  if (hasJasmine && !hasJest) return 'jasmine';
  if (hasJest && hasJasmine) return 'jest'; // Assume migration to Jest
  return 'unknown';
}

function countTests(content: string): number {
  const itMatches = content.match(/\bit\s*\(/g);
  return itMatches ? itMatches.length : 0;
}

function detectHttpMocking(content: string): boolean {
  return (
    content.includes('HttpTestingController') ||
    content.includes('HttpClient') ||
    content.includes('httpMock')
  );
}

function findDescribeBlocks(content: string): string[] {
  const describeRegex = /describe\s*\(\s*['"`]([^'"`]+)['"`]/g;
  const matches: string[] = [];
  let match;

  while ((match = describeRegex.exec(content)) !== null) {
    matches.push(match[1]);
  }

  return matches;
}

function findMockPatterns(content: string): string[] {
  const patterns: string[] = [];

  if (content.includes('jasmine.createSpyObj')) {
    patterns.push('jasmine.createSpyObj');
  }
  if (content.includes('jest.fn()')) {
    patterns.push('jest.fn()');
  }
  if (content.includes('jest.mock(')) {
    patterns.push('jest.mock()');
  }
  if (content.includes('provideMockStore')) {
    patterns.push('provideMockStore (NgRx)');
  }
  if (content.includes('MockComponent')) {
    patterns.push('MockComponent');
  }
  if (content.includes('NO_ERRORS_SCHEMA')) {
    patterns.push('NO_ERRORS_SCHEMA');
  }

  return patterns;
}

function detectAngularVersion(content: string): string | undefined {
  // Try to detect standalone components (Angular 14+)
  if (content.includes('standalone: true')) {
    return '14+';
  }
  // Try to detect signals (Angular 16+)
  if (content.includes('signal(') || content.includes('computed(')) {
    return '16+';
  }
  return undefined;
}

function findTestFiles(directory: string): string[] {
  if (!fs.existsSync(directory)) {
    return [];
  }

  const stat = fs.statSync(directory);
  if (stat.isFile()) {
    return isTestFile(directory) ? [directory] : [];
  }

  const files: string[] = [];
  const entries = fs.readdirSync(directory, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...findTestFiles(fullPath));
    } else if (entry.isFile() && isTestFile(fullPath)) {
      files.push(fullPath);
    }
  }

  return files;
}

function isTestFile(filePath: string): boolean {
  return filePath.endsWith('.spec.ts') || filePath.endsWith('.test.ts');
}

function analyzeDirectory(directory: string): AggregateAnalysis | { error: string } {
  const testFiles = findTestFiles(directory);

  if (testFiles.length === 0) {
    return {
      error: `No test files found in ${directory}`,
    };
  }

  const analyses = testFiles.map(analyzeTestFile);

  const frameworkCounts = {
    jest: analyses.filter(a => a.framework === 'jest').length,
    jasmine: analyses.filter(a => a.framework === 'jasmine').length,
  };

  const totalTests = analyses.reduce((sum, a) => sum + a.testCount, 0);
  const testBedCount = analyses.filter(a => a.usesTestBed).length;
  const httpMockingCount = analyses.filter(a => a.usesHttpMocking).length;
  const ngrxCount = analyses.filter(a => a.usesMockStore).length;

  let primaryFramework: 'jest' | 'jasmine' | 'mixed';
  if (frameworkCounts.jest > frameworkCounts.jasmine) {
    primaryFramework = 'jest';
  } else if (frameworkCounts.jasmine > frameworkCounts.jest) {
    primaryFramework = 'jasmine';
  } else {
    primaryFramework = 'mixed';
  }

  const commonPatterns: string[] = [];
  const allMockPatterns = analyses.flatMap(a => a.mockPatterns);
  const patternCounts = new Map<string, number>();
  allMockPatterns.forEach(pattern => {
    patternCounts.set(pattern, (patternCounts.get(pattern) || 0) + 1);
  });
  patternCounts.forEach((count, pattern) => {
    if (count >= testFiles.length * 0.3) { // Used in 30%+ of files
      commonPatterns.push(`${pattern} (${count} files)`);
    }
  });

  return {
    testFilesCount: testFiles.length,
    totalTests,
    primaryFramework,
    frameworkCounts,
    testBedUsage: `${testBedCount}/${testFiles.length} files`,
    httpMockingPattern: `${httpMockingCount}/${testFiles.length} files`,
    ngrxUsage: `${ngrxCount}/${testFiles.length} files`,
    testFiles: testFiles.slice(0, 10), // First 10 files
    namingPattern: detectNamingPattern(testFiles),
    commonPatterns,
  };
}

function detectNamingPattern(testFiles: string[]): string {
  const specCount = testFiles.filter(f => f.endsWith('.spec.ts')).length;
  const testCount = testFiles.filter(f => f.endsWith('.test.ts')).length;

  if (specCount > testCount) {
    return '*.spec.ts (Angular standard)';
  } else if (testCount > specCount) {
    return '*.test.ts';
  } else {
    return 'mixed';
  }
}

function printAnalysis(analysis: AggregateAnalysis | { error: string }): void {
  if ('error' in analysis) {
    console.log(`Error: ${analysis.error}`);
    console.log('Searched for: *.spec.ts, *.test.ts files');
    return;
  }

  console.log('='.repeat(70));
  console.log('ANGULAR TEST ANALYSIS');
  console.log('='.repeat(70));
  console.log(`\nTest Files Found: ${analysis.testFilesCount}`);
  console.log(`Total Tests: ${analysis.totalTests}`);
  console.log(`Primary Framework: ${analysis.primaryFramework}`);
  console.log(`  - Jest: ${analysis.frameworkCounts.jest} files`);
  console.log(`  - Jasmine: ${analysis.frameworkCounts.jasmine} files`);
  console.log(`Naming Pattern: ${analysis.namingPattern}`);
  console.log(`\nTestBed Usage: ${analysis.testBedUsage}`);
  console.log(`HTTP Mocking: ${analysis.httpMockingPattern}`);
  console.log(`NgRx (MockStore): ${analysis.ngrxUsage}`);

  if (analysis.commonPatterns.length > 0) {
    console.log(`\nCommon Mock Patterns:`);
    analysis.commonPatterns.forEach(pattern => {
      console.log(`  - ${pattern}`);
    });
  }

  console.log(`\nSample Test Files:`);
  analysis.testFiles.forEach(file => {
    console.log(`  - ${file}`);
  });

  if (analysis.testFilesCount > 10) {
    console.log(`  ... and ${analysis.testFilesCount - 10} more`);
  }

  console.log('='.repeat(70));
}

function printFileAnalysis(analysis: TestAnalysis): void {
  console.log('='.repeat(70));
  console.log(`ANALYSIS: ${analysis.file}`);
  console.log('='.repeat(70));
  console.log(`Framework: ${analysis.framework}`);
  console.log(`Test Count: ${analysis.testCount}`);
  console.log(`Uses TestBed: ${analysis.usesTestBed}`);
  console.log(`Uses HTTP Mocking: ${analysis.usesHttpMocking}`);
  console.log(`Uses NgRx MockStore: ${analysis.usesMockStore}`);

  if (analysis.angularVersion) {
    console.log(`Angular Version: ${analysis.angularVersion}`);
  }

  if (analysis.describeBlocks.length > 0) {
    console.log(`\nDescribe Blocks:`);
    analysis.describeBlocks.forEach(block => {
      console.log(`  - ${block}`);
    });
  }

  if (analysis.mockPatterns.length > 0) {
    console.log(`\nMock Patterns:`);
    analysis.mockPatterns.forEach(pattern => {
      console.log(`  - ${pattern}`);
    });
  }

  console.log('='.repeat(70));
}

function main(): void {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('Usage: ts-node test_analyzer.ts <test_directory_or_file>');
    console.log('\nExample:');
    console.log('  ts-node test_analyzer.ts src/app');
    console.log('  ts-node test_analyzer.ts src/app/components/user.component.spec.ts');
    process.exit(1);
  }

  const target = args[0];

  if (!fs.existsSync(target)) {
    console.error(`Error: Path '${target}' does not exist`);
    process.exit(1);
  }

  const stat = fs.statSync(target);

  if (stat.isFile()) {
    // Analyze single file
    const analysis = analyzeTestFile(target);
    printFileAnalysis(analysis);
  } else {
    // Analyze directory
    const analysis = analyzeDirectory(target);
    printAnalysis(analysis);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

export {
  analyzeTestFile,
  analyzeDirectory,
  TestAnalysis,
  AggregateAnalysis,
};
