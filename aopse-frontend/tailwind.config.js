import {join} from 'path';

import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import {skeleton} from '@skeletonlabs/tw-plugin';

/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'class',
    content: [
        './src/**/*.{html,js,svelte,ts}',
        join(require.resolve('@skeletonlabs/skeleton'), '../**/*.{html,js,svelte,ts}')
    ],
    theme: {
        extend: {
            fontFamily: {
                materialSymbols: ['Material Symbols Outlined']
            },
            keyframes: {
                scrollText: {
                    '0%': {transform: 'translateX(0)'},
                    '100%': {transform: 'translateX(-50%)'}
                }
            },
            animation: {
                'scroll-text': 'scrollText var(--scroll-time, 30s) linear infinite'
            }
        }
    },
    plugins: [
        forms,
        typography,
        skeleton({
            themes: {
                preset: [
                    {
                        name: 'skeleton',
                        enhancements: true
                    }
                ]
            }
        })
    ]
};
