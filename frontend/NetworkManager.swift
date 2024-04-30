//
//  NetworkManager.swift
//  FrontendBookApp
//
//  Created by Naif Albasheer on 29/04/2024.
//

import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    private let baseURL = "http://localhost:5000"  // Localhost for simulator testing

    func fetchAllBooks(completion: @escaping ([Book]?) -> Void) {
        guard let url = URL(string: "\(baseURL)/get-all-books") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                let decodedBooks = try? JSONDecoder().decode([Book].self, from: data)
                DispatchQueue.main.async {
                    completion(decodedBooks)
                }
            } else {
                print("Error fetching books: \(error?.localizedDescription ?? "Unknown error")")
                completion(nil)
            }
        }.resume()
    }
}
