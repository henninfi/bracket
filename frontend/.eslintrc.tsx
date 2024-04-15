module.exports = {
    extends: [
      'mantine',
      'plugin:@next/next/recommended',
      'plugin:jest/recommended',
    ],
    plugins: ['testing-library', 'jest'],
    overrides: [
      {
        files: ['**/?(*.)+(spec|test).[jt]s?(x)'],
        extends: ['plugin:testing-library/react'],
      },
    ],
    parserOptions: {
      project: './frontend/tsconfig.json',
    },
    rules: {
      'react/react-in-jsx-scope': 'off',
        "linebreak-style": "off",
        "arrow-body-style": "off"
    },
  };