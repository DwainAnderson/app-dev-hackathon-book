//
//  Book.swift
//  FrontendBookApp
//
//  Created by Naif Albasheer on 29/04/2024.
//

import Foundation

struct Book: Identifiable, Codable {
    var id: Int
    var title: String
    var author: String
    var publicationDate: String
    var genre: [String]
}
