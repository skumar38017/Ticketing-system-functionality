## Steps to Start a React Project with Create React App

1. **Install Dependencies (if not installed)**  
   This command will install all the necessary dependencies in the current repository:  
   ```sh
   yarn install
   ```

2. **Run the Development Server**  
   Start the React app in development mode:  
   ```sh
   yarn start
   ```  
   - Opens the app at [http://localhost:3000](http://localhost:3000).  
   - Auto-reloads on changes.  

3. **Run Tests (Optional)**  
   Execute tests in watch mode:  
   ```sh
   yarn test
   ```  

4. **Build for Production**  
   Create an optimized production build:  
   ```sh
   yarn build
   ```  
   - Generates minified files in the `build` folder.  
   - Ready for deployment.  

5. **Eject (Optional - Irreversible)**  
   If you need full control over configurations:  
   ```sh
   yarn eject
   ```  
   - Copies all dependencies and config files into the project.  
   - **Cannot be undone!** Use only if necessary.  

For additional details, refer to the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).