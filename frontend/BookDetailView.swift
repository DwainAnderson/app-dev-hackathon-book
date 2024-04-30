//
//  BookDetailView.swift
//  FrontendBookApp
//
//  Created by Naif Albasheer on 29/04/2024.
//

import Foundation
import SwiftUI

struct BookDetailView: View {
    var book: Book

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 10) {
                HStack {
                    Spacer()
                    Image(systemName: "book.fill")
                        .resizable()
                        .scaledToFit()
                        .frame(width: 100, height: 150)
                        .foregroundColor(.blue)
                    Spacer()
                }
                .padding(.top, 20)

                Text(book.title)
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)
                
                Text("By \(book.author)")
                    .font(.title2)
                    .fontWeight(.semibold)
                    .foregroundColor(.accentColor)
                
                Text("Published: \(book.publicationDate)")
                    .font(.body)
                    .foregroundColor(.secondary)
                
                Text("Genres")
                    .font(.headline)
                    .foregroundColor(.primary)
                
                ForEach(book.genre, id: \.self) { genre in
                    Text(genre)
                        .font(.subheadline)
                        .padding(4)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color.blue.opacity(0.2))
                        .cornerRadius(4)
                }

                Spacer()
            }
            .padding()
        }
        .navigationTitle(book.title)
        .navigationBarTitleDisplayMode(.inline)
    }
}

struct BookDetailView_Previews: PreviewProvider {
    static var previews: some View {
        BookDetailView(book: Book(id: 1, title: "Sample Book", author: "Author", publicationDate: "2021", genre: ["Fiction", "Mystery"]))
    }
}
