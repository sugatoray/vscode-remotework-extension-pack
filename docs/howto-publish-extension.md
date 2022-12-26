# How To Publish a VS Code Extension

1. Setup a Personal Access Token (PAT).

   - Create a publisher if you don't have one already.

     Open the extension manager with: 

     ```sh
     make vsce.open
     ```

   - Create a PAT:
     - label: `VSCE_PAT`
     - org: `all available`
     - expiry: `90 days`
   - Note down the PAT for later use.

     Open the webpage for creating/managing Azure tokens with:

     ```sh
     make vsce.token
     ``` 

2. Install `vsce` on you machine.

   - Install `node` on MacOS: `brew install node`
   - Install VSCE on any OS: `npm install -g vsce`

3. Check the validity of the PAT on your machine.
   
   - Store the PAT as:
     
     ```sh
     export VSCE_PAT=<your-pat-here>
     ```

   - Check the PAT:
     
     ```sh 
     vsce verify-pat -p $VSCE_PAT
     ```

     This should show:
     > *The Personal Access Token verification succeeded for the publisher 'sugatoray'.*

4. Setup VSCE publisher login.

   ```sh
   export VSCE_PUBLISHER=sugatoray
   vsce login $VSCE_PUBLISHER  
   ```

   Provide the VSCE_PAT you copied earlier.

5. Publish the extension via VSCE.

   ```sh
   vsce publish -p $VSCE_PAT
   ```

   Or, use (with already stored PAT):

   ```sh
   make pkg.publish
   ``` 

6. Show extension metadata.

   ```sh
   vsce show sugatoray.vscode-markdown-extension-pack
   ```

   Or, use:

   ```sh
   make vsce.metadata
   ```

7. Open Extension Page in Marketplace in the browser.

   ```sh
   make vsce.extn 
   ```

## Including Badges

> **Extension validation error**
>
> Error processing 'sugatoray.vscode-remotework-extension-pack' SVG reference in file '/extension/README.md'. 
> Your reference to the SVG image ‘https://vsmarketplacebadge.apphb.com/version/sugatoray.vscode-remotework-extension-pack.svg’ 
> is not supported. Please see https://aka.ms/vsmarketplace_badge for more details.

Use [this link](https://learn.microsoft.com/en-us/azure/devops/extend/develop/manifest?view=azure-devops#supported-badge-services) to see how badges can be included safely via `package.json`.
