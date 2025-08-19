(async function(){
  // configuration endpoint of the backend
  const CONFIG_URL = window.__CARBON_WIDGET_CONFIG_URL__ || (window.location.origin + '/widget-config');
  const ESTIMATE_URL = window.__CARBON_WIDGET_ESTIMATE_URL__ || (window.location.origin + '/estimate');
  const OPTIN_URL = window.__CARBON_WIDGET_OPTIN_URL__ || (window.location.origin + '/optin');

  try{
    const confRes = await fetch(CONFIG_URL);
    const config = await confRes.json();
    const placement = document.querySelector(config.placement || '#cart_container');
    if(!placement) return; 

    // Build widget DOM
    const box = document.createElement('div');
    box.style.border = '1px solid ' + (config.style?.border_color || '#2ecc71');
    box.style.padding = '12px';
    box.style.borderRadius = '6px';
    box.style.margin = '12px 0';
    box.style.display = 'flex';
    box.style.alignItems = 'center';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = 'carbon-offset-checkbox';
    checkbox.style.accentColor = '#2ecc71';

    const label = document.createElement('label');
    label.htmlFor = 'carbon-offset-checkbox';
    label.style.marginLeft = '8px';
    label.innerText = config.verbiage;

    const amountSpan = document.createElement('strong');
    amountSpan.style.marginLeft = '8px';

    box.appendChild(checkbox);
    box.appendChild(label);
    box.appendChild(amountSpan);

    placement.appendChild(box);

    // try to read Shopify cart JSON if available
    async function fetchCartFromShopify(){
      try{

        const res = await fetch('/cart-details');
        if(!res.ok) throw new Error('no cart');
        const cart = await res.json();
        
        const items = (cart.items || []).map(i => ({
          id: i.id,
          title: i.title,
          price: i.price,
          quantity: i.quantity,
          weight: i.grams
        }));
        return { cart: items, currency: cart.currency || 'USD' };
      }catch(e){
        return { cart: [] , currency: 'USD' };
      }
    }

    async function updateEstimate(){
      const cartPayload = await fetchCartFromShopify();
      if(!cartPayload.cart || cartPayload.cart.length === 0){
        amountSpan.innerText = '';
        return;
      }
      const res = await fetch(ESTIMATE_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(cartPayload)
      });
      if(!res.ok) return;
      const data = await res.json();
      amountSpan.innerText = ` $${data.estimated_offset.toFixed(2)} to offset my carbon footprint`;

      checkbox.dataset.latestEstimate = data.estimated_offset;
      checkbox.dataset.latestCart = JSON.stringify(cartPayload.cart);
    }

    checkbox.addEventListener('change', async function(e){
      if(this.checked){
        const payload = {
          merchant_id: window.location.hostname,
          customer_email: window.Shopify?.customer?.email || null,
          customer_name: window.Shopify?.customer?.first_name ? (window.Shopify.customer.first_name + ' ' + (window.Shopify.customer.last_name||'')) : null,
          cart: JSON.parse(this.dataset.latestCart || '[]'),
          estimated_offset: parseFloat(this.dataset.latestEstimate || 0)
        };
        await fetch(OPTIN_URL, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify(payload)
        });
      }
    });

    // initial estimate
    updateEstimate();

    // If cart changes, merchant themes usually change cart via XHR — poll periodically in this prototype
    setInterval(updateEstimate, 5000);

  }catch(err){
    console.error('Carbon widget error', err);
  }
})();
