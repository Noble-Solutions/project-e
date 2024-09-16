import { defineConfig } from 'vite'
// import { obfuscator } from 'rollup-obfuscator';
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: "0.0.0.0"
  },
  plugins: [
    react(),

    /*
    Ниже настройки обфускатора на случай если выкладывать код в продакшн
    чтобы усложнить его читаемость 
    */
   
  //   obfuscator({
  //     compact: true,
  //     controlFlowFlattening: true,
  //     controlFlowFlatteningThreshold: 0.75,
  //     deadCodeInjection: true,
  //     deadCodeInjectionThreshold: 0.4,
  //     debugProtection: false,
  //     debugProtectionInterval: 0,
  //     disableConsoleOutput: true,
  //     identifierNamesGenerator: 'hexadecimal',
  //     log: false,
  //     numbersToExpressions: true,
  //     renameGlobals: false,
  //     selfDefending: true,
  //     simplify: true,
  //     splitStrings: true,
  //     splitStringsChunkLength: 10,
  //     stringArray: true,
  //     stringArrayCallsTransform: true,
  //     stringArrayCallsTransformThreshold: 0.75,
  //     stringArrayEncoding: ['base64'],
  //     stringArrayIndexShift: true,
  //     stringArrayRotate: true,
  //     stringArrayShuffle: true,
  //     stringArrayWrappersCount: 2,
  //     stringArrayWrappersChainedCalls: true,
  //     stringArrayWrappersParametersMaxCount: 4,
  //     stringArrayWrappersType: 'function',
  //     stringArrayThreshold: 0.75,
  //     transformObjectKeys: true,
  //     unicodeEscapeSequence: true,
  //     include: ['**/*.js', '**/*.ts']
  // })
  ],
  optimizeDeps: {
    exclude: ['@reduxjs/toolkit']
  }
})