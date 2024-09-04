import React, { useState, useEffect, useRef } from 'react';

const RenderedHtmlSelectionApp = () => {
  const [selectedHtml, setSelectedHtml] = useState('');
  const [mathContent, setMathContent] = useState('');
  const htmlContentRef = useRef(null);
  const mathOutputRef = useRef(null);

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTML Example with Math</title>
    </head>
    <body>
        <h1>Hello, Math Lovers!</h1>
        <p>This is an HTML example for testing text selection and math rendering.</p>
        <ul>
          <li>Quadratic Formula: <span class="math">$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$</span></li>
          <li>Pythagorean Theorem: <span class="math">$a^2 + b^2 = c^2$</span></li>
          <li>Einstein's Mass-Energy Equivalence: <span class="math">$E = mc^2$</span></li>
        </ul>
        <p>More complex equation:</p>
        <p><span class="math">$\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}$</span></p>
        <p>Select any text or math formula to see the original HTML and rendered math!</p>
    </body>
    </html>
  `;

  useEffect(() => {
    // Load MathJax
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.9/MathJax.js?config=TeX-MML-AM_CHTML';
    script.async = true;
    document.head.appendChild(script);

    script.onload = () => {
      window.MathJax.Hub.Config({
        tex2jax: {
          inlineMath: [['$', '$']],
          processEscapes: true
        }
      });
      window.MathJax.Hub.Configured();
    };

    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const fragment = range.cloneContents();
        const tempDiv = document.createElement('div');
        tempDiv.appendChild(fragment);
        setSelectedHtml(tempDiv.innerHTML);

        // Extract math content
        const mathElements = tempDiv.getElementsByClassName('math');
        if (mathElements.length > 0) {
          const mathTexts = Array.from(mathElements).map(el => el.textContent);
          setMathContent(mathTexts.join(' '));
        } else {
          setMathContent('');
        }
      }
    };

    const contentElement = htmlContentRef.current;
    if (contentElement) {
      contentElement.addEventListener('mouseup', handleSelection);
    }

    return () => {
      if (contentElement) {
        contentElement.removeEventListener('mouseup', handleSelection);
      }
      document.head.removeChild(script);
    };
  }, []);

  useEffect(() => {
    if (mathContent && window.MathJax) {
      const wrappedContent = `<div>${mathContent}</div>`;
      mathOutputRef.current.innerHTML = wrappedContent;
      window.MathJax.Hub.Queue(["Typeset", window.MathJax.Hub, mathOutputRef.current]);
    } else {
      mathOutputRef.current.innerHTML = '';
    }
  }, [mathContent]);

  return (
    <div className="flex h-screen">
      <div 
        ref={htmlContentRef}
        className="w-1/2 h-full p-5 overflow-y-auto bg-white border-r border-gray-300"
        dangerouslySetInnerHTML={{ __html: htmlContent }}
      />
      <div className="w-1/2 p-5 flex flex-col bg-gray-50">
        <h2 className="text-xl mb-4">Selected HTML</h2>
        <textarea 
          className="w-full h-1/2 text-base p-2 border border-gray-300 rounded mb-4"
          value={selectedHtml}
          readOnly
        />
        <h2 className="text-xl mb-4">Rendered Math</h2>
        <div 
          ref={mathOutputRef}
          className="w-full h-1/3 p-2 border border-gray-300 rounded overflow-auto"
        />
      </div>
    </div>
  );
};

export default RenderedHtmlSelectionApp;
