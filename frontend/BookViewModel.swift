//
//  BookViewModel.swift
//  FrontendBookApp
//
//  Created by Naif Albasheer on 29/04/2024.
//

import Foundation

class BookViewModel: ObservableObject {
    @Published var books: [Book] = []

    func fetchBooks() {
        NetworkManager.shared.fetchAllBooks { [weak self] fetchedBooks in
            self?.books = fetchedBooks ?? []
        }
    }
}
