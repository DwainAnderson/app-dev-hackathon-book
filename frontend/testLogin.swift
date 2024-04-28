import UIKit

class LoginViewController: UIViewController {

    @IBOutlet weak var usernameTextField: UITextField!
    @IBOutlet weak var passwordTextField: UITextField!

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    @IBAction func loginButtonTapped(_ sender: UIButton) {
        guard let username = usernameTextField.text, !username.isEmpty,
              let password = passwordTextField.text, !password.isEmpty else {
            // Display an alert or message indicating that the fields are required
            return
        }

        // Call the login function here
        login(username: username, password: password)
    }

    func login(username: String, password: String) {
        let url = URL(string: "http://localhost:5000/login")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let parameters: [String: Any] = [
            "username": username,
            "password": password
        ]

        request.httpBody = try? JSONSerialization.data(withJSONObject: parameters)

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error: \(error)")
                // Display an alert or message indicating the error to the user
                return
            }

            guard let data = data,
                  let response = response as? HTTPURLResponse,
                  (200..<300).contains(response.statusCode) else {
                print("Invalid response or status code")
                // Display an alert or message indicating the invalid response or status code
                return
            }

            // Handle successful login response
            if let json = try? JSONSerialization.jsonObject(with: data, options: []),
               let result = json as? [String: Any],
               let message = result["message"] as? String {
                print(message)
                // Display an alert or message indicating successful login
            }
        }

        task.resume()
    }
}
