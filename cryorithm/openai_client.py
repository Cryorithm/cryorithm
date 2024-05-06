"""
Cryorithm™ | OpenAI Client
"""

# MIT License
#
# Copyright © 2024 Joshua M. Dotson (contact@jmdots.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import json
import openai


async def call_openai_api(data, api_key):
    client = openai.AsyncCompletion(api_key=api_key)

    try:
        response = await client.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": json.dumps(data)}],
            max_tokens=512,
            temperature=1.0,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.6,
            stream=True,
        )

        async for chunk in response.iter_chunks():
            print(chunk["choices"][0]["text"])

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
